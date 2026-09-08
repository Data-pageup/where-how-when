import os 
import certifi
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict, Annotated
import operator
import uuid

import psycopg
from psycopg.rows import dict_row

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)


class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

    is_travel_request: bool
    guardrail_message: str


# =========================
# Input Guardrail Agent
# =========================

def input_guardrail(state: TravelState):

    user_query = state["user_query"]

    prompt = f"""
You are an input validation guardrail for a travel planning AI.

Your job is to determine whether the user's request is related to travel.

User request:
{user_query}

A valid travel request can involve:

- Trip planning
- Flights
- Hotels
- Accommodation
- Tourist places
- Destinations
- Travel itinerary
- Transportation
- Travel budget
- Vacation planning
- Country or city travel information

If the request is travel-related, respond with exactly:

VALID

If the request is NOT related to travel, respond with:

INVALID

Do not explain anything.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a strict travel domain guardrail."
        ),
        HumanMessage(content=prompt)
    ])

    decision = response.content.strip().upper()

    is_valid = "VALID" in decision and "INVALID" not in decision

    if is_valid:

        return {
            "is_travel_request": True,
            "guardrail_message": "",
            "messages": [
                AIMessage(
                    content="Travel request validated."
                )
            ],
            "llm_calls": state.get("llm_calls", 0) + 1
        }

    return {
        "is_travel_request": False,

        "guardrail_message":
            "I can help with travel-related requests such as trip planning, flights, hotels, destinations, budgets, and itineraries.",

        "messages": [
            AIMessage(
                content=
                "I can help with travel-related requests such as trip planning, flights, hotels, destinations, budgets, and itineraries."
            )
        ],

        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# Guardrail Router
# =========================

def guardrail_router(state: TravelState):

    if state["is_travel_request"]:
        return "flight_agent"

    return "guardrail_response"


# =========================
# Flight Agent
# =========================

def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content="Flight results fetched.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }



# =========================
# Hotel Agent
# =========================

def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }




# =========================
# Itinerary Agent
# =========================

def itinerary_agent(state: TravelState):
    prompt = f"""
Create a complete travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}

Make the itinerary practical, budget-aware, and easy to follow.
"""

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# Guardrail Response Agent
# =========================

def guardrail_response(state: TravelState):

    return {
        "messages": [
            AIMessage(
                content=state["guardrail_message"]
            )
        ]
    }

# =========================
# Final Response Agent
# =========================

def final_agent(state: TravelState):
    final_prompt = f"""
Generate the final travel response for the user.

User Request:
{state['user_query']}

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Itinerary:
{state['itinerary']}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Day-by-Day Itinerary
5. Estimated Budget
6. Final Recommendations

Important:
- Be clear and practical.
- Mention that live flight API may not provide ticket prices if pricing is unavailable.
- Keep the response useful for real travel planning.
"""

    response = llm.invoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# =========================
# Build Graph
# =========================

graph = StateGraph(TravelState)


# Nodes

graph.add_node(
    "input_guardrail",
    input_guardrail
)

graph.add_node(
    "flight_agent",
    flight_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)

graph.add_node(
    "guardrail_response",
    guardrail_response
)


# START

graph.add_edge(
    START,
    "input_guardrail"
)


# Conditional Routing

graph.add_conditional_edges(
    "input_guardrail",

    guardrail_router,

    {
        "flight_agent": "flight_agent",
        "guardrail_response": "guardrail_response"
    }
)


# Travel Workflow

graph.add_edge(
    "flight_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)


# Invalid Request Workflow

graph.add_edge(
    "guardrail_response",
    END
)


# =========================
# PostgreSQL Checkpointer
# =========================
DATABASE_URL = get_database_url()

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

travel_graph = graph.compile(checkpointer=checkpointer)



# =========================
# Function for FastAPI
# =========================

def run_travel_agent(user_input: str, thread_id: str | None = None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    result = travel_graph.invoke(
    {
        "messages": [
            HumanMessage(content=user_input)
        ],

        "user_query": user_input,

        "flight_results": "",

        "hotel_results": "",

        "itinerary": "",

        "llm_calls": 0,

        "is_travel_request": False,

        "guardrail_message": ""
    },

    config=config
)

    final_answer = result["messages"][-1].content

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0),
    }