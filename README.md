# Agentic Last-Mile Delivery Coordinator

## Overview
Agentic Last-Mile Delivery Coordinator is a multi-agent, LLM-powered AI system designed for autonomous last-mile disruption resolution.
It intelligently coordinates between merchants, drivers, and customers, making human-like decisions and showing transparent reasoning.

## Features
- 🧠 **Multi-Agent Orchestration** – Coordinator + Specialist Agents
- 🗂 **Context Memory** – Past cases inform present decisions
- 🛠 **Tool-Driven Reasoning** – Simulated logistics APIs (`check_traffic()`, `get_merchant_status()`, etc.)
- ⚡ **Two-Speed Decision Making** – Immediate reaction + deep optimization
- 🗺 **Digital Twin Output** – Real-time map-ready JSON updates
- 🚀 **Zero-Shot Tool Adoption** – Learns and uses new tools mid-operation

## Wow Factor 
1. **Feels Human** – Friendly Grab voice, empathy in decision-making
2. **Adapts in Real-Time** – Handles unexpected tools & scenarios
3. **Visually Explains Itself** – Step-by-step reasoning cards
4. **Multi-Agent Teamwork** – Different “experts” working together

## Setup
```bash
# Clone the repository
git clone <repo-url>
cd project-synapse

# Install dependencies
pip install -r requirements.txt

# Run the application with a scenario
# (Requires OPENAI_API_KEY to be set as an environment variable)
python src/main.py "There is a damaged packaging dispute for order order-789."

# Or run in mock mode (no API key required)
python src/main.py "There is a damaged packaging dispute for order order-789." --mock-llm
```

## Usage

To run the agent, provide a disruption scenario as a command-line argument. The agent can be run in mock mode (which simulates LLM calls and requires no API key) using the `--mock-llm` flag.

### Example Scenarios

#### Overloaded Restaurant
```bash
python src/main.py "My order from merchant-456 is taking a long time." --mock-llm
```

#### Damaged Packaging Dispute
```bash
python src/main.py "There is a dispute over a spilled drink for order-789." --mock-llm
```

#### Recipient Unavailable
```bash
python src/main.py "The recipient for order-abc is unavailable at the delivery address." --mock-llm
```

#### Sudden Traffic Obstruction
```bash
python src/main.py "There is a major traffic obstruction on the route to the airport." --mock-llm
```

## Project Structure
```
.
├── README.md          # This file
├── requirements.txt   # Project dependencies
├── src                # Source code
│   ├── main.py        # Main application entry point (CLI)
│   ├── agent          # Agent-related code
│   │   └── coordinator.py # The main Coordinator agent logic
│   ├── memory         # Context memory components (placeholder)
│   │   └── context.py
│   └── tools          # Simulated API tools
│       └── logistics.py
└── tests              # Unit tests
    ├── test_agents.py
    ├── test_memory.py
    └── test_tools.py
```

## Agent Design

The core of this project is the `Coordinator` agent, an AI-powered decision-maker built using the **LangChain** framework.

### Architecture
The agent uses a **ReAct (Reasoning and Acting)** architecture. This means it operates in a loop:
1.  **Reason:** Based on the input and its memory, the LLM "thinks" about what to do next. This "chain of thought" is visible in the output.
2.  **Act:** If it decides to gather more information, it selects one of its available **Tools** (e.g., `get_merchant_status`) and specifies the input for it.
3.  **Observe:** The agent executes the tool and receives an **Observation** (the tool's output). This new information is added to its memory.

This loop continues until the agent has enough information to form a final plan, which it then outputs.

### Prompt Engineering
The agent's behavior is guided by a detailed system prompt located in `src/agent/coordinator.py`. This prompt defines:
-   Its **persona** (an intelligent logistics coordinator).
-   Its available **tools** and how to use them.
-   Specific **protocols** for handling different types of scenarios (e.g., disputes, unavailable recipients).

This structured prompting is key to ensuring the agent behaves in a reliable and predictable way.
