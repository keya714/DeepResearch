from mcp.server.fastmcp import FastMCP
from agents import run_research

mcp=FastMCP("crew_research")

@mcp.tool()
def crew_research(query: str) -> str:
    """
    Conduct comprehensive research on a given topic using a multi-agent system.
    
    Args:
        query (str): The research topic or question.
    
    Returns:
        str: A well-structured document with citations and source URLs.
    """
    return run_research(query)

if __name__ == "__main__":
    mcp.run(transport="stdio")