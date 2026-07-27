import streamlit as st

from ui_streamlit.backend import ask_agent


def render_chat():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["role"] == "assistant":

                if message.get("tool_output"):
                    st.subheader("📊 Results")
                    st.markdown(message["tool_output"])
                    st.divider()

                answer = message["content"]

                if answer.startswith("AI Analysis"):
                    answer = answer.replace("AI Analysis", "", 1).strip()

                if answer.startswith("AI Analysis"):
                    answer = answer.replace("AI Analysis", "", 1).strip()

                st.subheader("🧠 AI Analysis")
                st.markdown(answer)

                if message.get("agent"):
                    st.caption(
                        f"{message['agent']} • {message['time']:.2f} sec"
                )

            else:
                st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask anything about stocks..."
    )

    if not st.session_state.messages:
        st.info(
            "👋 Ask me about company fundamentals, annual reports, stock prediction, or compare two companies."
        )

    if not prompt:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("📊 Analyzing your request..."):

            tool_output, answer, agent_used, execution_time = ask_agent(prompt)

        if tool_output:
            st.subheader("📊 Results")
            st.markdown(tool_output)
            st.divider()

        st.subheader("🤖 AI Analysis")
        st.markdown(answer)

        st.caption(
            f"{agent_used} • {execution_time:.2f} sec"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "tool_output": tool_output,
            "agent": agent_used,
            "time": execution_time,
        }
    )