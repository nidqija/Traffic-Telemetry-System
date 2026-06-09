import pandas as pd
import asyncio
from ai_factory.factory_manager import AiFactoryManager
import streamlit as st




ai_config = {"model_name" : "gemma3:1b"}
ai_agent = AiFactoryManager.get_agent("ollama", ai_config)


def ai_agent_page():
    st.title("AI Agent Query Interface")
    st.write("Ask questions about the traffic data and get insights!")

    user_question = st.text_input("Enter your question about the traffic data:")

    if st.button("Ask AI Agent"):
        if user_question.strip() == "":
            st.warning("Please enter a question before submitting.")
        else:
            with st.spinner("AI Agent is thinking..."):
                response = ai_agent.ask_questions(user_question)
                st.subheader("AI Agent Response:")
                st.write(response)

    else:
        st.info("Type a question and click the button to get insights from the AI agent.")


if __name__ == "__main__":
    ai_agent_page()