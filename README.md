# AI-Travel-Assistant-Project-Guide
Local AI Travel Agent is an offline assistant built during my Labmentix internship. Powered by LangChain, Streamlit, and a local LLM via Ollama, it queries JSON databases and the Open-Meteo REST API using Pydantic validation. It includes a custom engine that instantly converts itineraries into PowerPoint slides, running in 18s under 2GB RAM.

Key Features
100% Local Inference: Zero reliance on proprietary cloud APIs (OpenAI/Anthropic). Absolute data privacy with ₹0.00 token cost.

Agentic ReAct Framework: Uses the LLM as a cognitive orchestrator to parse user intent, evaluate constraints, select appropriate tools, and synthesize unstructured data.

Robust Multi-Tool Orchestration: Successfully binds and triggers heterogeneous tools:

search_flights: Local JSON-based flight schedule database query.

Google Hotels: Local hotel inventory data parser.

discover_places: Regional points-of-interest mapping.

get_weather_forecast: Asynchronous REST API telemetry fetching live weather data from Open-Meteo.

Fail-Safe Schema Validation: Enforces strict parameter controls using Pydantic Validation Models to completely eliminate argument hallucinations and token loops in small-scale models.

Dynamic PPTX Compilation Engine: On-the-fly markdown parsing that transforms the generated itinerary into an Office Open XML (.pptx) presentation binary stream for instant download.

Tech Stack & Dependencies
Language: Python 3.10 - 3.12

Frameworks: LangChain, LangChain-Ollama, Streamlit

Inference Engine: Ollama Core Daemon (qwen2.5:3b)

Document Utility: Python-PPTX

Network Client: Requests (HTTP REST Telemetry)

Quick Start & Installation
1. Clone the Repository
 git clone https://github.com/yourusername/Local-AI-Travel-Agent.git
cd Local-AI-Travel-Agent

2. Install Project Dependencies
pip install -r requirements.txt
(Make sure langchain-ollama, python-pptx, and streamlit are included in your requirements file)

3. Initialize and Download the Local Model
Ensure you have Ollama running in the background, then pull the optimized model:
ollama run qwen2.5:3b
(Once the download completes, type /exit to return to your normal terminal).

4. Run the Application
Launch the dashboard locally via Streamlit:
streamlit run app.py

Evaluation & Metrics
Token Optimization: INT4 quantization compresses model size to under 2.0 GB, allowing the agent to perform natively on standard laptops without VRAM constraints.

Pipeline Latency: The agent successfully parses local databases, calls external weather APIs, formats the layout, and renders the itinerary in ~18.4 seconds.

Operational Cost: Absolute reduction in API maintenance and generation costs to ₹0.00.
