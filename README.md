# Project Synapse – Agentic Last-Mile Delivery Coordinator

## Overview
Project Synapse is a multi-agent, LLM-powered AI system designed for autonomous last-mile disruption resolution.
It intelligently coordinates between merchants, drivers, and customers, making human-like decisions and showing transparent reasoning.

## Features
- 🧠 **Multi-Agent Orchestration** – Coordinator + Specialist Agents
- 🗂 **Context Memory** – Past cases inform present decisions
- 🛠 **Tool-Driven Reasoning** – Simulated logistics APIs (`check_traffic()`, `get_merchant_status()`, etc.)
- ⚡ **Two-Speed Decision Making** – Immediate reaction + deep optimization
- 🗺 **Digital Twin Output** – Real-time map-ready JSON updates
- 🚀 **Zero-Shot Tool Adoption** – Learns and uses new tools mid-operation

## Wow Factor (Hackathon Winning Points)
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
