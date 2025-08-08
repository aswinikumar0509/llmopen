import sys
import os
import re
from io import BytesIO

# Fix import issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from langchain.memory import ConversationBufferMemory
from src.components.retrival import retrieve_and_score_query
from src.components.tools import summarizer_fn, legal_drafting_fn

# Initialize memory
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(return_messages=True)

if "retrieved_answer" not in st.session_state:
    st.session_state.retrieved_answer = ""

if "retrieved_sources" not in st.session_state:
    st.session_state.retrieved_sources = []

# Page config
st.set_page_config(page_title="Legal RAG Assistant", page_icon="⚖️", layout="wide")

# Sidebar memory viewer + download
with st.sidebar:
    st.markdown("### 🧠 Memory Panel")
    show_memory = st.checkbox("Show Conversation Memory", value=False)

    if show_memory:
        st.markdown("#### 📜 Previous Messages")
        messages = st.session_state.chat_memory.chat_memory.messages
        if messages:
            for msg in messages:
                role = "🧑 You" if msg.type == "human" else "🤖 Assistant"
                st.markdown(f"**{role}:** {msg.content}")
        else:
            st.info("No memory yet.")

    st.markdown("---")
    st.markdown("### 💾 Download Conversation")

    def generate_pdf_from_memory(messages):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        for msg in messages:
            role = "You" if msg.type == "human" else "Assistant"
            content = str(msg.content or "")

            # Make links clickable in Assistant responses
            if role == "Assistant":
                content = re.sub(r'(https?://\S+)', r'<a href="\1" color="blue">\1</a>', content)

            story.append(Paragraph(f"<b>{role}:</b> {content}", styles["Normal"]))
            story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return buffer

    if st.session_state.chat_memory.chat_memory.messages:
        pdf_buffer = generate_pdf_from_memory(st.session_state.chat_memory.chat_memory.messages)
        st.download_button(
            label="📄 Download Chat History (PDF)",
            data=pdf_buffer,
            file_name="vakki_chat_history.pdf",
            mime="application/pdf"
        )
    else:
        st.info("No conversation yet to download.")

# Main UI
st.title("⚖️ Vakki: Legal Research Assistant")
st.markdown("Ask a legal question, summarize answers, or draft legal documents")

query = st.text_area(
    "Enter your legal question or drafting request:",
    height=90,
    placeholder="Ask Vakki..."
)

# Three columns for actions
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    retrieve_button = st.button("🔍 Retrieve Answer")

with col2:
    summarize_button = st.button("📝 Summarize Answer")

with col3:
    draft_button = st.button("📄 Draft Legal Document")

# ✅ Retrieve Answer
if retrieve_button and query.strip():
    with st.spinner("Processing your query..."):
        try:
            answer, similarity, faithfulness, sources = retrieve_and_score_query(
                query, memory=st.session_state.chat_memory
            )
            st.session_state.retrieved_answer = answer
            st.session_state.retrieved_sources = sources

            st.success("✅ Answer Retrieved")
            st.markdown(f"**🧠 Answer:**\n\n{answer}")
            st.markdown(f"**🔁 Similarity Score (Query ↔ Answer):** `{similarity:.4f}`")
            st.markdown(f"**📚 Faithfulness Score (Context ↔ Answer):** `{faithfulness:.4f}`")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

# ✅ Summarize Retrieved Answer
elif summarize_button:
    if not st.session_state.retrieved_answer:
        st.warning("❗ No answer available to summarize. Please retrieve an answer first.")
    else:
        with st.spinner("Summarizing the retrieved answer..."):
            try:
                summary = summarizer_fn(st.session_state.retrieved_answer)
                st.success("📝 Summary Generated")
                st.markdown(f"**✂️ Summary:**\n\n{summary}")
            except Exception as e:
                st.error(f"❌ Failed to summarize: {e}")

# ✅ Draft Legal Document
elif draft_button:
    if not query.strip():
        st.warning("❗ Please enter drafting instructions first.")
    else:
        with st.spinner("Drafting your legal document..."):
            try:
                draft = legal_drafting_fn(query)
                st.success("📄 Draft Generated")
                st.markdown(f"**🖋 Draft:**\n\n{draft}")
            except Exception as e:
                st.error(f"❌ Failed to draft: {e}")

else:
    st.info("Enter a question above and click 'Retrieve Answer', 'Summarize Answer', or 'Draft Legal Document'.")
