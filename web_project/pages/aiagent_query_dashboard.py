import streamlit as st
from ai_factory.factory_manager import AiFactoryManager
from ai_factory.cloudflare_worker_factory import CloudflareWorkerFactory

# ------------------- AI AGENT SETUP ------------------- #

# We can easily switch between different AI agents by changing the agent_type and config parameters
agent_type = "cloudflare_worker"  # Change to "ollama" if you want
agent_config = {
    "model_name": "@cf/meta/llama-3-8b-instruct"  # Optional: specify a different model if desired
}
try:
    ai_agent = AiFactoryManager.get_agent(agent_type, agent_config)
except Exception as e:
    st.error(f"❌ Error initializing AI agent: {e}")
    st.stop()  # Stop execution if the agent fails to initialize


# ------------------- PAGE CONFIG ------------------- #
st.set_page_config(
    page_title="Traffic AI Agent",
    page_icon="🚦",
    layout="centered"
)

# ------------------- CUSTOM CSS ------------------- #
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0rem;
    }

    .subtitle {
        text-align: center;
        color: #808080;
        margin-bottom: 2rem;
    }

    .result-box {
        padding: 1rem;
        border-radius: 12px;
        background-color: #262730;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)


def ai_agent_page():
    # ---------- Header ----------
    st.markdown(
        "<div class='main-title'>🚦 Traffic Data AI Agent</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='subtitle'>Ask natural language questions about your traffic light database.</div>",
        unsafe_allow_html=True
    )

    # ---------- Example Questions ----------
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - How many times was the red light active?
        - What is the latest traffic record?
        - How many green light activations are there?
        - How many total records are stored?
        - Count the records where only the red light is active.
        """)

    # ---------- User Input ----------
    user_question = st.text_input(
        "📝 Enter your question",
        placeholder="e.g. How many times was the red light active?"
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        ask_button = st.button(
            "🚀 Ask AI Agent",
            use_container_width=True
        )

    # ---------- Query Execution ----------
    if ask_button:
        if not user_question.strip():
            st.warning(" Please enter a question before submitting.")
            return

        with st.spinner(" AI Agent is generating SQL..."):
            try:
                response = ai_agent.ask_questions(user_question)

                generated_sql = response if isinstance(response, str) else "N/A"

                st.success("✅ Query generated successfully!")

                st.markdown("### Generated SQL")
                st.code(generated_sql, language="sql")

                # Optional: show raw response for debugging
                with st.expander(" Debug Information"):
                    st.write(response)

            except Exception as e:
                st.error(f"❌ Error while generating SQL:\n\n{e}")

    else:
        st.info("👆 Enter a question above and press **Ask AI Agent**.")


if __name__ == "__main__":
    ai_agent_page()