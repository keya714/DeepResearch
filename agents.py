import os
from crewai import LLM, Agent, Task, Crew, Process
from linkup import LinkUpSearchTool

# def get_llm_client():
#     llm = ChatOpenAI(
#         model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
#         temperature=0,
#         openai_api_base="https://openrouter.ai/api/v1",
#         openai_api_key=os.environ["OPENAI_API_KEY"]
#     )
#     return llm

os.environ["GEMINI_API_KEY"] = "AIzaSyCAY09nK6OMxZtcRnMoWQCCxMwJBoEUFOE"

def get_llm_client():
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise RuntimeError("Must set GEMINI_API_KEY to use Gemini model")

    # CrewAI's native LLM wrapper
    llm = LLM(
        model="gemini/gemini-2.5-flash",  # 👈 important: use provider prefix
        api_key=gemini_key,
        temperature=0,
    )
    return llm

def run_research(query: str) -> str:
    client = get_llm_client()
    
    web_searcher = Agent(
        role="Web Searcher",
        goal="Retrieve relevant information with citations (source URLs).",
        backstory="Expert searcher; forwards results to Research Analyst only.",
        verbose=True,
        allow_delegation=True,
        tools=[LinkUpSearchTool()],
        llm=client,  # Added LLM to web_searcher
    )

    search_task = Task(
        description=f"Search for comprehensive information about: {query}.",
        agent=web_searcher,
        expected_output="Detailed information with citations-source URLs.",
        tools=[LinkUpSearchTool()],
    )

    research_analyst = Agent(
        role="Research Analyst",
        goal="Turn raw information into structured insights with citations (source URLs).",
        backstory="Expert analyst, can delegate fact-checks to Web Searcher; hands final output to Technical Writer.",
        verbose=True,
        allow_delegation=True,
        llm=client,
    )

    analysis_task = Task(
        description=f"Analyze search results, extract insights, and verify facts.",
        agent=research_analyst,
        expected_output="Structured insights with verified facts and source URLs",
        context=[search_task]
    )

    technical_writer = Agent(
        role="Technical Writer",    
        goal="Create clear, concise, and well-structured documents with citations (source URLs).",
        backstory="Expert writer; composes final documents based on Research Analyst's insights.",
        verbose=True,
        allow_delegation=False,
        llm=client,  # Added LLM to technical_writer
    )

    writing_task = Task(
        description=f"Write a clear, organised response based on research.",
        agent=technical_writer,
        expected_output="Well-structured document with citations-source URLs.",
        context=[analysis_task]
    )

    crew = Crew(
        agents=[web_searcher, research_analyst, technical_writer],
        tasks=[search_task, analysis_task, writing_task],
        verbose=True,
        process=Process.sequential,  # Fixed: Process.sequential instead of Process.SEQUENTIAL
        llm=client,  # Added LLM to crew
    )

    result = crew.kickoff(inputs={"query": query})
    return str(result)