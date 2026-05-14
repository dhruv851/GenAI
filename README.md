# GenAI Exploration

A hands-on learning repository exploring core GenAI concepts — prompt engineering, agentic AI, memory, voice, and graph-based workflows — built with OpenAI and LangGraph.

---

## Projects

### Hello World
Basic OpenAI API integration to get started with chat completions.

### Prompts
Prompt engineering techniques using OpenAI:
- `zero.py` — Zero-shot prompting
- `few.py` — Few-shot prompting with structured JSON output
- `cot.py` — Chain of Thought (CoT) reasoning with step-by-step planning

### Weather Agent
An AI agent that uses **Chain of Thought + Tool Use** to answer queries. It can fetch live weather data and run system commands via structured JSON reasoning steps (PLAN → TOOL → OBSERVE → OUTPUT).

### Voice Agent
A voice-enabled AI agent that:
- Listens to microphone input (via `speech_recognition`)
- Transcribes speech using OpenAI **Whisper**
- Reasons using CoT with tool use
- Responds with text-to-speech using OpenAI **TTS**

### Memory Agent (`mem_agent`)
A persistent memory chatbot powered by:
- **Mem0** for memory management
- **Qdrant** (vector store) for semantic search
- **Neo4j** (graph store) for relationship-based memory
- **GPT-4o** for responses

### LangGraph
Stateful chatbot workflows using **LangGraph**:
- `chat.py` / `chat2.py` — Basic stateful graph chatbots
- `chat_checkpoint.py` — Conversation checkpointing with **MongoDB** for persistent multi-turn memory

### Image
Vision model example — sends an image URL to **GPT-4o** and generates a caption.

---

## Tech Stack

- **OpenAI** (GPT-4o, GPT-4.1-mini, Whisper, TTS)
- **LangGraph** + **LangChain**
- **Mem0** — Memory layer
- **Qdrant** — Vector database
- **Neo4j** — Graph database
- **MongoDB** — Checkpoint storage
- **Pydantic** — Structured output parsing
- **Python** 3.13

---

## Setup

```bash
# Clone the repo
git clone https://github.com/dhruv851/GenAI.git
cd GenAI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

---

## Environment Variables

```
OPENAI_API_KEY=your_openai_api_key
```

For `mem_agent`, also add:
```
NEO_CONNECTION_URI=your_neo4j_uri
NEO_USERNAME=neo4j
NEO_PASSWORD=your_password
```
