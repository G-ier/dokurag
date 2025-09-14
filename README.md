_Version 2.0.1 · 250914_

# DokuRAG

Document RAG (Retrieval-Augmented Generation) with CLI tool for managing PDF documents and querying them with AI.

## Quick Start

DokuRAG has a simple command-line interface for uploading PDF documents to Weviate from the folder 'data' and querying them with an AI assistant. You can also upload and query at the same time with one command.

How to use this experimental RAG system is very simple. Follow the conceptual steps below to use the system easily:
1. Upload documents to the "data" folder - Store command (-s)
2. Prompt the LLM with a question or a mini-task. - Ask database command (-pd)

In the "Basic usage" section you will find the specific commands for the above steps.

## Architecture

![DokuRAG Architecture](assets/dokurag_architecture.png)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd dokurag

# Install dependencies - if using uv
uv sync
docker compose up -d

# Install dependencies - if using normal pip and venv
python -m venv venv       # 1. Create a new env named "venv"
source venv/bin/activate  # 2. Activate it (Unix/macOS)
# OR
venv\Scripts\activate     # On Windows
pip install -r requirements.txt # 3. Install
# AND THEN
docker compose up -d


```

## Environment Setup

Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=key
BASE_URL=https://openrouter.ai/api/v1
MODEL=o3
TOKENIZERS_PARALLELISM=false
```


Replace `your_api_key_here` with your actual OpenRouter API key.

You can also replace the API Key with an OpenRouter API Key. the .env should then look like this:
```
OPENROUTER_API_KEY=key
BASE_URL=https://openrouter.ai/api/v1
MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free
TOKENIZERS_PARALLELISM=false
```

Both methods have been tested. OpenAI will be the preferred method.

Hint: If you have a preferred embedding model from HuggingFace, then set the EMBEDDING_MODEL to that specific model. The default one used will be a multilingual embedding model.

### Basic Usage

```bash
# Basic LLM proompt - does not have any document retreival capability
uv run main.py -p "What is machine learning?"

# Prompt with document context from the database set up
uv run main.py -pd "Explain this concept"

# Run specific test
uv run main.py -t name
uv run --env-file .env python -m pytest tests/specific_test.py -v -s

# Run all tests
uv run main.py -ta

# Check database size - amount of chunks
uv run main.py -c

# Store all the documents in the "data" folder in the database
uv run main.py -s

# Delete all the data in the database
uv run main.py -d

# Show help and all available options
uv run main.py -h
```

### Command Options

- `-d FILE_PATH` - Upload a single PDF file to the vector database
- `-db FOLDER_PATH` - Upload multiple PDF files from a folder to the vector database
- `-p TEXT` - Prompt the LLM with the given text
- `-pd TEXT` - Prompt the LLM with text and relevant documents from the database
- `-h` - Show help message with usage examples

## Future Additions

- MMR reranking
- Collections management for organization of document knowledge-bases
- Add ingestion for images
- Evaluation suite and regression tests for retrieval and QA quality
- Pluggable embedding and LLM providers with retries, rate-limit handling, and fallbacks
- Observability
- Lightweight web UI for browsing, searching, and chatting over documents
- UI for managing uploaded docs
- Scalability improvements:
    - clustered design for weviate instances with sharding/replication
    - streaming chunks for better ingestion efficiency