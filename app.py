import streamlit as st
from utils.log import logger
from utils.ai_assist import upload_to_vectors_db, get_llm_answer

# Set up the page configuration
st.set_page_config(page_title="PDF AI Assistant",
                   layout="wide", initial_sidebar_state='collapsed')

# Page header
st.header("🚀 AI PDF Assistant")

# Custom styling for markdown
st.markdown(
    """
    <style>
    p {
        margin-bottom: 3px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    

# Sidebar with tabs for Upload and History
tab1, tab2 = st.sidebar.tabs(["📁 Upload", "📜 History"])

# Upload Tab
with tab1:
    st.title("⬆️ Upload a PDF")
    uploaded_file = st.file_uploader("Upload PDFs into Database", type="pdf")

# History Tab
with tab2:
    if len(st.session_state.chat_history) == 0:
        st.write("No history found!")
    else:
        for chat in st.session_state.chat_history[::-1]:
            st.write(f"**💬 {chat['question']}**")
            st.write(f"🔥 {chat['answer']}")
            st.write(f"**🪙 Tokens burned:** {chat['tokens_burned']}")
            st.divider()

# Save uploaded file
save_path = ""
if uploaded_file:
    uploaded_file_name = uploaded_file.name
    logger.info(f"Uploaded file: {uploaded_file_name}")
    with open(uploaded_file_name, mode='wb') as w:
        w.write(uploaded_file.getvalue())
    save_path = uploaded_file_name
    

# Upload to vectors database
if save_path:
    try:
        upload_to_vectors_db(save_path=save_path)
    except Exception as e:
        logger.error(f"Error uploading file to vectors database: {e}")

# User input for questions
st.subheader("💬 Ask")
st.write("Ask your questions regarding your uploaded PDFs. Our AI will assist you with all the PDF's information.")
user_question = st.text_input(
    "Enter your question:", placeholder="Enter your question to receive answers from all uploaded PDFs.", label_visibility="collapsed")

answer = ""
# Get AI answer and update chat history
if user_question:
    try:
        question, answer, tokens = get_llm_answer(user_question=user_question)
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "tokens_burned": tokens,
        })
        logger.info(f"question asked: {question} (Tokens burned: {tokens})")
    except Exception as e:
        logger.error(f"Error getting AI answer: {e}")

# Display answer
if answer:
    st.subheader("🌟 Answer")
    st.subheader(answer)
