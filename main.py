
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,START,END
from langchain_core.tools import tool
from typing import TypedDict,Annotated
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from prompts import research_prompt,assembly_prompt,template_builder_prompt,supervisor_prompt

from dotenv import load_dotenv
load_dotenv()


llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-pro')

# web search tool 
from langchain_tavily import TavilySearch
web_search_tool = TavilySearch(max_results=3)

# File management tool
from langchain_community.agent_toolkits import FileManagementToolkit

working_directory = './'

file_management_tools =FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["read_file", "write_file", "list_directory"]
).get_tools()


read_tool, write_tool, list_tool = file_management_tools


#arxiv
import arxiv

@tool("arxiv_search")
def arxiv_search(query: str,max_results: int = 5) -> str:
    """
    Searches arXiv for papers matching the query.
    - query: keywords, authors or title
    - max_results: number of papers to return
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        papers = []
        for result in search.results():
            pdf_url = result.pdf_url if hasattr(result,"pdf_url") else result.entry_id.replace("abs","pdf")
            papers.append(
                f"Title: {result.title}\n"
                f"Authors: {','.join(a.name for a in result.authors)}\n"
                f'Published: {result.published.date()}\n'
                f"Abstract: {result.summary.strip()}\n"
                f"Link: {result.entry_id}\n"
                f"PDF: {pdf_url}\n"
                + "-"*80

            )
        if not papers:
            return f"No results found for '{query}"
        
        return "\n".join(papers)
    except Exception as e:
        return f"Error during arXiv search: {e}"
    

#wikipedia
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(load_all_available_meta=True))

from langchain_community.tools import YouTubeSearchTool
youtube_tool = YouTubeSearchTool()


from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


research_agent = create_react_agent(
    model=llm,
    tools = [arxiv_search,wikipedia_tool,youtube_tool,read_tool,write_tool , list_tool,web_search_tool],
    prompt=(research_prompt),
    name="research_agent",
)


assembly_agent = create_react_agent(
    model=llm,
    tools=[read_tool,write_tool, list_tool],
    prompt=(assembly_prompt),
    name="assembly_agent",
)


template_builder_agent = create_react_agent(
    model=llm,
    tools=[read_tool,write_tool, list_tool],
    prompt=(template_builder_prompt),
    name="template_builder_agent",
)


from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model



supervisor = create_supervisor(
    model=llm,
    agents=[assembly_agent, research_agent,template_builder_agent],
    prompt=(supervisor_prompt),
    add_handoff_back_messages=True,
    output_mode="last_message"
).compile()





