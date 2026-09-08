# 🌍 GoAnywhere AI

### by Amirtha Ganesh R

### A Multi-Agent Travel Planning System Built with LangGraph

GoAnywhere AI is an AI-powered multi-agent travel planning system that helps users generate complete and practical travel plans.

The application uses multiple specialized agents to search for flight information, discover hotels, generate personalized travel itineraries, and produce a structured final travel plan.

The complete workflow is orchestrated using **LangGraph**, while **PostgreSQL** is used for persistent workflow checkpointing and conversation state management. The application can also be integrated with **LangSmith** for tracing, debugging, and observability.

---

# 🚀 Features

- 🤖 Multi-Agent AI Architecture
- ✈️ Flight Information Agent
- 🏨 Hotel Search Agent
- 🗺️ AI Travel Itinerary Generation
- 🧠 Final Response Agent
- 🔀 LangGraph Workflow Orchestration
- 💾 PostgreSQL Persistent Checkpointing
- 🧵 Thread-Based Conversation Persistence
- 🔎 Tavily Search Integration
- ✈️ AviationStack Flight API Integration
- ⚡ FastAPI Backend
- 🎨 Modern Travel Planning UI
- 📋 Copy Generated Travel Plans
- 📄 Download Travel Plans as PDF
- 📊 LangSmith Observability Support
- 🛡️ Extensible Guardrail Architecture

---

# 🧠 System Architecture

```text
                              USER
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Frontend UI       │
                     │  HTML + CSS + JS    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      FastAPI        │
                     │      Backend        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     LangGraph       │
                     │ Multi-Agent Workflow│
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Flight Agent     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     Hotel Agent     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Itinerary Agent   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Final Response    │
                     │       Agent         │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ PostgreSQL Checkpoint│
                     │   Persistent State   │
                     └──────────┬──────────┘
                                │
                                ▼
                              USER
```

---

# 🤖 Multi-Agent Architecture

GoAnywhere AI uses multiple specialized agents.

Each agent is responsible for a specific part of the travel planning workflow.

The agents communicate through a shared LangGraph state.

---

## ✈️ Flight Agent

The Flight Agent processes the user's travel request and retrieves flight-related information.

The agent uses the flight search tool to gather available flight information.

### Responsibilities

- Extract travel-related flight requirements
- Process the user's travel request
- Search for available flights
- Retrieve flight-related information
- Pass flight results to downstream agents

### Workflow

```text
User Travel Request
        │
        ▼
   Flight Agent
        │
        ▼
 Flight Search Tool
        │
        ▼
 Flight Results
        │
        ▼
 Next Agent
```

### Agent Flow

```text
User Query
    │
    ▼
"Plan a 7-day Japan trip
 from Chennai"
    │
    ▼
Flight Agent
    │
    ▼
search_flights(query)
    │
    ▼
Flight Information
```

The flight results are stored in the shared LangGraph state.

```text
TravelState
    │
    └── flight_results
```

---

# 🏨 Hotel Agent

The Hotel Agent searches for hotel and accommodation information related to the user's travel request.

The agent uses Tavily Search to retrieve relevant accommodation information.

### Responsibilities

- Search for hotels
- Find accommodation recommendations
- Retrieve travel-related hotel information
- Search for destination-specific accommodation
- Pass hotel information to downstream agents

### Workflow

```text
User Travel Request
        │
        ▼
    Hotel Agent
        │
        ▼
    Tavily Search
        │
        ▼
Hotel Information
        │
        ▼
Next Agent
```

### Example

```text
User Request:
Plan a 7-day trip to Japan.

        │
        ▼

Hotel Agent

        │
        ▼

Search Query:
Best hotels for 7-day Japan trip

        │
        ▼

Tavily Search

        │
        ▼

Hotel Results
```

The hotel information is stored in the shared state.

```text
TravelState
    │
    └── hotel_results
```

---

# 🗺️ Itinerary Agent

The Itinerary Agent combines information collected by the previous agents and generates a complete travel itinerary.

The agent receives information from:

- User travel request
- Flight Agent
- Hotel Agent

The LLM then generates a practical and budget-aware travel itinerary.

### Responsibilities

- Create a complete travel schedule
- Organize day-by-day activities
- Consider flight information
- Consider hotel information
- Suggest sightseeing activities
- Create a practical itinerary
- Consider the user's budget

### Workflow

```text
                 Flight Results
                       │
                       │
                       ▼
                ┌───────────────┐
                │   Itinerary   │
                │     Agent     │
                └───────┬───────┘
                        │
                        │
                       ▼
                Travel Itinerary
                        ▲
                        │
                        │
                 Hotel Results
```

### Input

```text
User Query
+
Flight Results
+
Hotel Results
```

### Output

```text
Complete AI Travel Itinerary
```

The generated itinerary is stored in the shared state.

```text
TravelState
    │
    └── itinerary
```

---

# 🧠 Final Response Agent

The Final Response Agent generates the final response shown to the user.

It combines all information generated by the previous agents.

### Input

The Final Response Agent receives:

- User Request
- Flight Results
- Hotel Results
- Travel Itinerary

### Output Structure

The final response is formatted into the following sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Day-by-Day Itinerary
5. Estimated Budget
6. Final Recommendations

### Workflow

```text
User Request
     │
     ▼
Flight Results
     │
     ▼
Hotel Results
     │
     ▼
Travel Itinerary
     │
     ▼
Final Response Agent
     │
     ▼
Structured Travel Plan
     │
     ▼
User
```

---

# 🔀 LangGraph Workflow

GoAnywhere AI uses LangGraph to orchestrate the complete multi-agent workflow.

The workflow consists of:

- Nodes
- Edges
- Shared State
- Agent Communication
- Persistent Checkpointing

### Current Workflow

```text
START
  │
  ▼
Flight Agent
  │
  ▼
Hotel Agent
  │
  ▼
Itinerary Agent
  │
  ▼
Final Response Agent
  │
  ▼
END
```

### LangGraph Architecture

```text
                    ┌───────────┐
                    │   START   │
                    └─────┬─────┘
                          │
                          ▼
                 ┌────────────────┐
                 │  Flight Agent  │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │   Hotel Agent  │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │Itinerary Agent │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │  Final Agent   │
                 └───────┬────────┘
                         │
                         ▼
                    ┌───────────┐
                    │    END    │
                    └───────────┘
```

---

# 🧩 Shared LangGraph State

The application uses a shared state to allow agents to exchange information.

The state contains:

```text
TravelState
│
├── messages
│
├── user_query
│
├── flight_results
│
├── hotel_results
│
├── itinerary
│
└── llm_calls
```

### State Flow

```text
User Query
    │
    ▼
TravelState
    │
    ├──────────────► Flight Agent
    │                    │
    │                    ▼
    │              flight_results
    │
    ├──────────────► Hotel Agent
    │                    │
    │                    ▼
    │               hotel_results
    │
    ├──────────────► Itinerary Agent
    │                    │
    │                    ▼
    │                 itinerary
    │
    └──────────────► Final Agent
                         │
                         ▼
                   Final Response
```

---

# 🛡️ Guardrails Architecture

GoAnywhere AI is designed to support travel-domain guardrails.

Guardrails can be used to validate user input before expensive tools, APIs, and LLM calls are executed.

The purpose of the guardrail layer is to ensure that the multi-agent workflow remains focused on travel-related tasks.

### Proposed Guardrail Flow

```text
User Query
    │
    ▼
Input Guardrail
    │
    ▼
Is the request travel-related?
    │
 ┌──┴─────┐
 │        │
YES       NO
 │        │
 ▼        ▼
Travel     Return Safe
Workflow   Response
 │
 ▼
Flight Agent
 │
 ▼
Hotel Agent
 │
 ▼
Itinerary Agent
 │
 ▼
Final Agent
 │
 ▼
END
```

### Examples of Valid Requests

```text
Plan a 7-day trip to Japan from Chennai.
```

```text
Find hotels in Dubai.
```

```text
Plan a budget trip to Thailand.
```

```text
What flights are available from Chennai to Singapore?
```

### Examples of Non-Travel Requests

```text
Write Python code.
```

```text
Explain machine learning.
```

```text
Solve this mathematics problem.
```

A guardrail layer can prevent unrelated requests from unnecessarily entering the travel agent workflow.

---

# 💾 PostgreSQL Persistent Memory and Checkpointing

GoAnywhere AI uses PostgreSQL together with LangGraph's `PostgresSaver`.

The purpose of PostgreSQL in this application is persistent workflow checkpointing.

The database stores LangGraph execution checkpoints and workflow state.

### Technologies Used

```text
PostgreSQL
+
Psycopg
+
LangGraph PostgresSaver
=
Persistent Agent State
```

---

# 🗄️ Why PostgreSQL?

Without persistent checkpointing:

```text
User Request
     │
     ▼
Workflow Runs
     │
     ▼
Workflow Ends
     │
     ▼
State Lost
```

With PostgreSQL checkpointing:

```text
User Request
     │
     ▼
LangGraph Workflow
     │
     ▼
PostgresSaver
     │
     ▼
PostgreSQL Database
     │
     ▼
Checkpoint Stored
     │
     ▼
Persistent Workflow State
```

---

# 🧵 Thread-Based Persistent Memory

Each workflow execution is associated with a unique thread ID.

Example:

```text
user_a1b2c3d4e5f6
```

The thread ID is passed to LangGraph during invocation.

### Thread Flow

```text
User
 │
 ▼
Generate / Receive Thread ID
 │
 ▼
LangGraph Configuration
 │
 ▼
PostgreSQL Checkpointer
 │
 ▼
Persistent Workflow State
```

### Conceptual Configuration

```text
configurable
    │
    └── thread_id
```

The thread ID allows LangGraph checkpoints to be associated with a specific workflow or conversation.

---

# 🗄️ PostgreSQL Architecture

```text
                GoAnywhere AI
                      │
                      ▼
                  Psycopg
                      │
                      ▼
           PostgreSQL Connection
                      │
                      ▼
          LangGraph PostgresSaver
                      │
                      ▼
          Persistent Checkpoints
                      │
                      ▼
           Workflow State History
```

The application initializes the PostgreSQL checkpointer before compiling the LangGraph workflow.

```text
PostgreSQL Connection
        │
        ▼
PostgresSaver
        │
        ▼
setup()
        │
        ▼
Graph Compilation
        │
        ▼
Persistent Workflow
```

---

# 📊 LangSmith Observability

GoAnywhere AI can use LangSmith for tracing and observability.

LangSmith provides visibility into the execution of the multi-agent system.

It can be used to inspect:

- LLM calls
- Agent execution
- Prompts
- Responses
- Workflow execution paths
- Latency
- Token usage
- Errors
- Debugging information

---

# 🔍 LangSmith Workflow

```text
User Request
      │
      ▼
LangGraph Workflow
      │
      ├──── Flight Agent
      │
      ├──── Hotel Agent
      │
      ├──── Itinerary Agent
      │
      └──── Final Agent
      │
      ▼
 LangSmith Tracing
      │
      ▼
Execution Observability
```

---

# 🧠 Why LangSmith?

Multi-agent systems can become difficult to debug because multiple agents, tools, APIs, and LLM calls are involved.

LangSmith can help answer questions such as:

```text
Which agent produced this response?
```

```text
Which prompt was sent to the LLM?
```

```text
How long did the agent execution take?
```

```text
Where did the workflow fail?
```

```text
How many LLM calls were made?
```

```text
What was the complete execution path?
```

This makes LangSmith useful for debugging, monitoring, and evaluating the multi-agent workflow.

---

# 🔎 Tavily Search Integration

The application uses Tavily Search for retrieving travel-related information.

In the current architecture, Tavily is primarily used by the Hotel Agent.

### Flow

```text
User Travel Request
        │
        ▼
    Hotel Agent
        │
        ▼
Tavily Search Query
        │
        ▼
Hotel Information
        │
        ▼
LangGraph State
```

---

# ✈️ AviationStack Integration

The Flight Agent uses a flight search tool to retrieve flight-related information.

The application is designed to integrate with AviationStack for flight data.

### Flow

```text
User Travel Request
        │
        ▼
   Flight Agent
        │
        ▼
 Flight Search Tool
        │
        ▼
 AviationStack API
        │
        ▼
 Flight Information
        │
        ▼
LangGraph State
```

---

# 🧠 Groq LLM

GoAnywhere AI uses Groq for LLM inference.

The LLM is responsible for generating intelligent travel content.

### Current Model

```text
openai/gpt-oss-120b
```

### The LLM is used for

- Travel itinerary generation
- Travel planning
- Budget-aware recommendations
- Final response generation
- Structured travel responses

---

# ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application Development |
| FastAPI | Backend API |
| LangGraph | Multi-Agent Workflow Orchestration |
| LangChain | LLM Integration |
| Groq | LLM Inference |
| PostgreSQL | Persistent Checkpoint Storage |
| Psycopg | PostgreSQL Connectivity |
| PostgresSaver | LangGraph Checkpoint Persistence |
| LangSmith | Tracing and Observability |
| Tavily | Travel and Hotel Search |
| AviationStack | Flight Information |
| HTML | Frontend Structure |
| CSS | Frontend Design |
| JavaScript | Frontend Interaction |

---

# 📂 Project Structure

```text
goanywhere-ai-langgraph/
│
├── app.py
│
├── backend.py
│
├── requirements.txt
│
├── README.md
│
├── .env
│
├── .gitignore
│
├── templates/
│   │
│   └── index.html
│
├── static/
│   │
│   ├── style.css
│   │
│   └── script.js
│
└── tools/
    │
    ├── tavily_tool.py
    │
    └── flight_tool.py
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Move into the project directory.

```bash
cd goanywhere-ai-langgraph
```

---

# 2. Create a Virtual Environment

Using uv:

```bash
uv venv
```

### Windows PowerShell

```bash
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bash
.venv\Scripts\activate
```

---

# 3. Install Dependencies

Using uv:

```bash
uv pip install -r requirements.txt
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

DATABASE_URL=your_postgresql_connection_string

LANGCHAIN_TRACING_V2=true

LANGCHAIN_API_KEY=your_langsmith_api_key

LANGCHAIN_PROJECT=goanywhere-ai
```

---

# 🔑 Environment Variables Explained

| Variable | Purpose |
|---|---|
| GROQ_API_KEY | Access to Groq LLM |
| TAVILY_API_KEY | Access to Tavily Search |
| AVIATIONSTACK_API_KEY | Access to Flight API |
| DATABASE_URL | PostgreSQL Connection |
| LANGCHAIN_TRACING_V2 | Enable LangSmith Tracing |
| LANGCHAIN_API_KEY | LangSmith API Key |
| LANGCHAIN_PROJECT | LangSmith Project Name |

---

# ▶️ Running the Application

Start the FastAPI application.

```bash
uvicorn app:app --reload
```

Open the application in your browser.

```text
http://127.0.0.1:8000
```

---

# 🌐 Complete Application Flow

```text
                         USER
                           │
                           ▼
                    Frontend Interface
                           │
                           ▼
                      FastAPI API
                           │
                           ▼
                  run_travel_agent()
                           │
                           ▼
                    LangGraph Workflow
                           │
                           ▼
                    Flight Agent
                           │
                           ▼
                    Flight Search Tool
                           │
                           ▼
                    Hotel Agent
                           │
                           ▼
                     Tavily Search
                           │
                           ▼
                  Itinerary Agent
                           │
                           ▼
                  Groq LLM Generation
                           │
                           ▼
                 Final Response Agent
                           │
                           ▼
              PostgreSQL Checkpointing
                           │
                           ▼
                  Structured Response
                           │
                           ▼
                         USER
```

---

# 🛠️ Example Execution

### User Request

```text
Plan a complete 7-day trip to Japan from Chennai including flights, hotels and sightseeing under 2 lakhs.
```

### Execution Flow

```text
1. User submits travel request
        │
        ▼
2. Flight Agent retrieves flight information
        │
        ▼
3. Hotel Agent searches accommodation information
        │
        ▼
4. Itinerary Agent creates a day-by-day plan
        │
        ▼
5. Final Agent formats the complete response
        │
        ▼
6. PostgreSQL stores workflow checkpoints
        │
        ▼
7. Final travel plan returned to user
```

---

# 📈 Key Engineering Concepts Demonstrated

```text
Multi-Agent Systems
        +
LangGraph Orchestration
        +
Shared Agent State
        +
External API Integration
        +
LLM Reasoning
        +
PostgreSQL Checkpointing
        +
Thread-Based Persistence
        +
LangSmith Observability
        =
GoAnywhere AI
```

---

# 🔮 Future Improvements

Planned improvements include:

- 🔀 Parallel agent execution
- ✈️ Flight and Hotel Agents running simultaneously
- 🌦️ Weather Agent
- 🗺️ Destination Recommendation Agent
- 💰 Budget Agent
- 🛡️ Production Input Guardrails
- 🛡️ Output Guardrails
- ✈️ Real-Time Flight Pricing
- 🏨 Hotel Booking Integration
- 🗺️ Interactive Maps
- 👤 User Authentication
- ❤️ Saved Trips
- 🧵 Multi-Turn Conversation Support
- 🐳 Docker Containerization
- ☁️ AWS Cloud Deployment
- 📊 LangSmith Agent Evaluation
- 🔁 Human-in-the-Loop Travel Approval

---

# 🐳 Future Deployment Architecture

```text
                       Internet
                           │
                           ▼
                    Frontend Client
                           │
                           ▼
                     FastAPI Server
                           │
                           ▼
                   LangGraph Workflow
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Groq LLM       Tavily     AviationStack
             │
             ▼
        LangSmith Tracing
             │
             ▼
         PostgreSQL
      Persistent State
```

---

# 🎯 Project Objective

GoAnywhere AI demonstrates how multi-agent AI systems can be applied to a real-world travel planning problem.

The project combines modern AI engineering concepts with backend development and persistent workflow management.

The system demonstrates:

- Artificial Intelligence
- Large Language Models
- Multi-Agent Systems
- LangGraph
- Agent-Oriented Workflows
- Shared State Management
- External API Integration
- Persistent Checkpointing
- PostgreSQL
- Thread-Based Workflows
- LangSmith Observability
- FastAPI Backend Development

---

# 👨‍💻 Author

## Amirtha Ganesh R

M.Sc. Data Science

Areas of Interest:

- Data Science
- Machine Learning
- Deep Learning
- Generative AI
- Large Language Models
- LangChain
- LangGraph
- Multi-Agent Systems
- AI Agents
- MLOps

---

# 📌 Disclaimer

GoAnywhere AI is designed to assist users with travel planning.

Flight and hotel information depends on the availability and limitations of external APIs and search providers.

Users should verify important information before making travel or booking decisions.

This includes:

- Flight availability
- Ticket prices
- Hotel availability
- Visa requirements
- Local regulations
- Travel restrictions
- Currency conversion
- Booking conditions

---

# ⭐ Support

If you found this project interesting, consider giving the repository a star.

---

# 🌍 GoAnywhere AI

### Plan Anywhere. Explore Everywhere. Powered by Multi-Agent AI and LangGraph.
