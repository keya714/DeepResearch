import os
from typing import Type
from pydantic import BaseModel, Field
# Remove the circular import - you'll need to install the linkup package separately
# from linkup import LinkupClient
from crewai.tools import BaseTool

# You'll need to implement or import LinkupClient properly
class LinkupClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def search(self, query: str, depth: str = "standard", output_type: str = "searchResults") -> str:
        # Implement your search logic here
        return f"Search results for: {query}"

class LinkUpSearchInput(BaseModel):
    # Input schema for LinkUp Search Tool.
    query: str = Field(description="Search query")
    depth: str = Field(default="standard", description="Depth of search: 'standard' or 'deep'")
    output_type: str = Field(
        default="searchResults",
        description="Output type: 'searchResults' or 'sourcedAnswer'"
    )

class LinkUpSearchTool(BaseTool):
    name: str = "LinkupSearch"
    description: str = (
        "Useful for searching the web using LinkUp. "
    )
    args_schema: Type[BaseModel] = LinkUpSearchInput

    def _run(self, query: str, depth: str = "standard", output_type: str = "searchResults") -> str:
        client = LinkupClient(api_key="249b33ce-6a05-4b95-bcfa-8c323d0b98a6")
        response = client.search(query=query, depth=depth, output_type=output_type)
        return response

     