import streamlit as st

from context.context_manager import ConversationContext
from ui_streamlit.sidebar import render_sidebar
from ui_streamlit.chat import render_chat


st.set_page_config(
    page_title="Multi-Agent AI for Corporate Finance",
    page_icon="📈",
    layout="wide"
)


def initialize_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent_used" not in st.session_state:
        st.session_state.agent_used = ""

    if "execution_time" not in st.session_state:
        st.session_state.execution_time = 0.0
    
    ConversationContext.initialize()


def main():

    initialize_session()

    render_sidebar()

    st.title("📈 Multi-Agent AI for Corporate Finance Assistant")

    st.caption(
        "AI Powered - Corporate Annual Reports • Finance • Stock Analysis • AI Predictions"
    )

    render_chat()


if __name__ == "__main__":
    main()