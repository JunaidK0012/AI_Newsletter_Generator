from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import streamlit as st
from pathlib import Path
from langgraph.types import Command
from datetime import datetime

# Import your supervisor workflow
from main import supervisor  

# working directories
research_dir = Path("Research/AI Newsletter")
raw_dir = Path("raw_newsletter/AI Newsletter")
output_dir = raw_dir

st.set_page_config(page_title="AI Newsletter Multi-Agent System", layout="wide")

st.title("📰 AI Newsletter Multi-Agent System")

st.sidebar.header("Controls")

if st.sidebar.button("🚀 Run Newsletter Workflow"):

    log_box = st.empty()
    research_placeholder = st.empty()
    newsletter_placeholder = st.empty()
    email_placeholder = st.empty()

    logs = []  # keep all logs


    for stream_mode, chunk in supervisor.stream(
        {"messages": [("user", "Start newsletter pipeline.")]}
        ,{"recursion_limit": 50},
        stream_mode=["updates", "messages"]
    ):
        if stream_mode == "updates":
             
            for node, data in chunk.items():
                # Collect log
                logs.append("----------------------------------")
                logs.append(f"🔄 **Update from node:** {node}")
                logs.append("----------------------------------")

            if "messages" in data:
                for msg in data["messages"]:
                    if isinstance(msg, AIMessage):
                        # Avoid duplicate supervisor summaries
                        if node == "supervisor" and "pipeline has been successfully completed" in msg.content:
                            continue  
                        logs.append(f"🤖 : {msg.content}")

                    elif isinstance(msg, ToolMessage):
                        logs.append(f"🔧 Used tool: {msg.name} -> {msg.content}")

            # 🔄 Refresh Logs (scrollable)
            with log_box.container():
                st.subheader("📡 Live Workflow Logs")
                st.markdown(
                    "<div style='height:300px; overflow-y:scroll; "
                    "background-color:#111; color:#0f0; padding:10px; "
                    "font-family:monospace; border-radius:8px;'>"
                    + "<br>".join(logs) +
                    "</div>",
                    unsafe_allow_html=True
                )

            # 🔄 Refresh Research Outputs
            if research_dir.exists():
                files = list(research_dir.glob("*.md"))
                with research_placeholder.container():
                    st.header("📂 Research Outputs")
                    for f in files:
                        with st.expander(f"📄 {f.name}", expanded=False):
                            st.markdown(f.read_text(encoding="utf-8"))

            # 🔄 Refresh Final Newsletter
            final_newsletter = raw_dir / "AI_Newsletter_This_Week.md"
            with newsletter_placeholder.container():
                st.header("📝Raw Newsletter (Markdown)")
                if final_newsletter.exists():
                    with st.expander("📄 Preview Final Newsletter", expanded=True):
                        st.markdown(final_newsletter.read_text(encoding="utf-8"))
                else:
                    st.info("No final newsletter generated yet.")


            # 🔄 Refresh Email Outputs
            with email_placeholder.container():
                st.header("📧 Newsletter Draft")
                if output_dir.exists():
                    for f in output_dir.iterdir():
                        if f.suffix == ".html":
                            with st.expander(f"🌐 {f.name}"):
                                try:
                                    html_content = f.read_text(encoding="utf-8")
                                    st.components.v1.html(html_content, height=600, scrolling=True)
                                except UnicodeDecodeError:
                                    st.error(f"⚠️ Could not decode {f.name}. Try opening manually.")
                        elif f.suffix == ".txt":
                            with st.expander(f"📜 {f.name}"):
                                try:
                                    text_content = f.read_text(encoding="utf-8")
                                    st.text(text_content)
                                except UnicodeDecodeError:
                                    st.error(f"⚠️ Could not decode {f.name}. Try opening manually.")
                else:
                    st.info("No email outputs generated yet.")


    st.success("🎉 All agents finished their tasks!")

