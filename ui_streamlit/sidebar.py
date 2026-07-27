import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("📈 Corporate Financial Assistant")

        st.divider()

        st.subheader("🚀 Features")

        st.success("Company Fundamentals")
        st.success("Annual Report Analysis")
        st.success("Stock Price Prediction")
        st.success("Company Comparison")
        st.success("Context-Aware Conversation")

        st.divider()

        st.subheader("Sample Questions You May Ask...")

        st.markdown("""
        **Fundamentals**
        - What is ROE of Infosys?

        **Annual Reports**
        - Summarize TCS annual report

        **Prediction**
        - Predict RELIANCE stock price

        **Comparison**
        - Compare RELIANCE and TCS
        """)

        st.divider()

        if st.button("🗑 Clear Conversation", use_container_width=True):

            # Clear chat messages
            st.session_state.messages = []

            # Reset UI state
            st.session_state.agent_used = ""
            st.session_state.execution_time = 0.0

            # Clear conversation context
            st.session_state.conversation_context = {
                "companies": [],
                "last_question": None,
                "last_tool": None,
            }

            st.rerun()