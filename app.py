import streamlit as st
import time
import csv
from datetime import datetime
import sys
import os
from pathlib import Path

# Path for benchmark results
BENCHMARK_CSV = "benchmark_results.csv"

def log_benchmark(query, success, elapsed_time):
    timestamp = datetime.now().isoformat()
    st.write(f"Logging: {timestamp}, Success: {success}, Time: {elapsed_time:.2f}")
    with open(BENCHMARK_CSV, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, query, success, f"{elapsed_time:.2f}"])
        csvfile.flush()  # force flush to disk

# Page config
st.set_page_config(
    page_title="MCP Server Tester",
    page_icon="🔬",
    layout="wide"
)
st.title("🔬 MCP Server Tester")
st.markdown("Test and benchmark your CrewAI Research MCP Server")

# Debug: Show current working directory
st.write("Current working directory:", os.getcwd())

# Sidebar for file checks
st.sidebar.header("Server Status")
st.sidebar.markdown("---")
for fname in ["research_server.py", "agents.py", "linkup.py"]:
    exists = Path(fname).exists()
    if exists:
        st.sidebar.success(f"✅ {fname} found")
    else:
        st.sidebar.error(f"❌ {fname} not found")
st.sidebar.markdown("---")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Research Query")
    with st.form("research_form"):
        query = st.text_area(
            "Enter your research question:",
            placeholder="e.g., Explain the theory of relativity with examples and applications",
            height=100
        )
        submitted = st.form_submit_button("🔍 Start Research", type="primary")
        if submitted and query:
            with st.spinner("Conducting research..."):
                try:
                    from agents import run_research
                    start_time = time.time()
                    result = run_research(query)
                    elapsed = time.time() - start_time
                    success = bool(result and len(str(result).strip()) > 0)
                    log_benchmark(query, success, elapsed)

                    st.success("Research completed!")
                    st.markdown("---")
                    st.subheader("Research Results")
                    st.markdown(result)
                    st.info(f"Elapsed time: {elapsed:.2f} seconds")
                    st.info(f"Success: {'Yes' if success else 'No'}")
                except Exception as e:
                    st.error(f"Error running research: {str(e)}")
                    st.code(str(e))
                    log_benchmark(query, False, 0)

with col2:
    st.header("MCP Server Info")
    st.subheader("Configuration")
    st.code("""
Server: crew_research
Command: uv run research_server.py
Transport: stdio
    """)
    if st.button("🧪 Test Server Import"):
        try:
            import research_server
            st.success("✅ Server imports successfully")
            if hasattr(research_server, 'mcp'):
                st.success("✅ MCP instance found")
                if hasattr(research_server.mcp, 'tools'):
                    st.info(f"📋 Tools available: {len(research_server.mcp.tools)}")
                else:
                    st.warning("⚠️ No tools attribute found")
            else:
                st.error("❌ No MCP instance found")
        except Exception as e:
            st.error(f"❌ Import failed: {str(e)}")

    st.subheader("Manual Test")
    if st.button("🔬 Start Server (Manual)"):
        st.info("Starting server in stdio mode...")
        st.code("python research_server.py")
        st.warning("This will start the server in stdio mode. Use Ctrl+C to stop.")

st.markdown("---")
st.markdown("**MCP Server Tester** - Test & benchmark your CrewAI Research MCP Server")
st.markdown("Make sure your `mcp.json` is properly configured in Cursor settings.")

with st.expander("🔧 Debug Information"):
    st.subheader("File Structure")
    current_dir = Path(".")
    files = list(current_dir.glob("*.py"))
    for file in files:
        st.text(f"📄 {file.name}")

    st.subheader("Python Path")
    st.code(sys.path)

    st.subheader("Environment Variables")
    env_vars = {k: v for k, v in os.environ.items() if 'GOOGLE' in k or 'API' in k}
    if env_vars:
        for k, v in env_vars.items():
            st.text(f"{k}: {v[:10]}..." if len(v) > 10 else f"{k}: {v}")
    else:
        st.text("No relevant environment variables found")
