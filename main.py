
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from prompts import research_prompt,assembly_prompt,template_builder_prompt,supervisor_prompt
from tools import web_search_tool,read_tool,write_tool,list_tool,wikipedia_tool,youtube_tool,arxiv_search
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-pro')

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

supervisor = create_supervisor(
    model=llm,
    agents=[research_agent,assembly_agent,template_builder_agent],
    prompt=(supervisor_prompt),
    add_handoff_back_messages=True,
    output_mode="last_message"
).compile()





