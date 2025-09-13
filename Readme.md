# DeepResearch

DeepResearch is a multi-agent AI research assistant platform leveraging CrewAI to conduct comprehensive topic research using coordinated agents for web searching, analysis, and writing.

## Features

- Multi-agent orchestration with specialized agents for web search, research analysis, and technical writing.
- Integration with LinkUp API for live web search results.
- Interactive Streamlit UI for submitting research queries and displaying structured results.
- Benchmark logging of request success and elapsed time in `benchmark_results.csv`.
- Load testing capabilities to evaluate Streamlit server performance via `test.py`.

## Project Structure

- `agents.py`: Implements multi-agent coordination for the research pipeline.
- `linkup.py`: Defines the LinkUpSearchTool using LinkUp search API.
- `app.py`: Streamlit app for user queries, result display, and benchmarking.
- `research_server.py`: MCP server exposing the research tool for external calls.
- `test.py`: Load test script for the Streamlit server.
- `benchmark_results.csv`: Logs performance metrics per research query.
- `__pycache__/`: Bytecode cache (ignored in usage).

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Required packages: CrewAI, Streamlit, Pydantic, etc.
- API keys (export as environment variables):
  - `GEMINI_API_KEY` for Gemini LLM
  - LinkUp API key inside `linkup.py`

### Installation

pip install -r requirements.txt

### Running the Application

Start the Streamlit interface:

streamlit run app.py

Access the web UI at `http://localhost:8501` to enter research questions.

### Running the MCP Server

python research_server.py

Starts the research server for tool integration.

### Load Testing

python test.py

Runs concurrent requests to benchmark Streamlit server throughput.

## Usage

- Enter a research query in the Streamlit app.
- Multi-agent system fetches and analyzes web data, then writes a structured, cited document.
- Performance metrics are logged automatically.

## Environment Variables

- `GEMINI_API_KEY`: Gemini LLM API key (required).
- `LinkUp_API_KEY`: LinkUp API key (required).

## Notes

- LinkUp API integration requires complete client implementation.
- Agents run in sequential process ensuring detailed and factual research output.
- Streamlit UI provides server status indicators and debugging tools.

## License

Specify your license here (e.g., MIT License).
