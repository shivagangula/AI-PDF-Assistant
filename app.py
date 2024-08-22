import streamlit as st
import os
from ai_assist import upload_to_vectors_db, get_llm_answer


import streamlit as st


st.set_page_config(page_title="PDF AI Assist", layout="wide", initial_sidebar_state='collapsed')
st.header("**🚀 AI PDF Assistant**")
st.markdown(
    """
    <style>
    p{
        margin-bottom:3px !important;
    }
    
    
    </style>
    """,
    unsafe_allow_html=True
)

# int chat histrory
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

tab1, tab2 = st.sidebar.tabs(["📁 Upload","📜 History"])


with tab1:
    st.title("⬆️ Upload a PDF")
    uploaded_file = st.file_uploader("Upload PDFs into Databas", type="pdf")

with tab2:
    if len(st.session_state.chat_history) == 0:
       st.write("No history found !.")
 
    
    for chat in st.session_state.chat_history[::-1]:
        st.write(f"**💬 {chat['question']}**")
        st.write(f"✅ {chat['answer']}")
        st.write(f"**🪙 Tokens burned:** {chat['tokens_burned']}")
        st.divider()
    
    


    
save_path = ""

if uploaded_file:

    uploaded_file_name = uploaded_file.name
    with open(uploaded_file_name, mode='wb') as w:
        w.write(uploaded_file.getvalue())
    save_path = uploaded_file_name

if save_path:
    upload_to_vectors_db(save_path=save_path)


    
    
    
st.subheader("💬 Ask")
st.write("Ask your questions regrading your uploaded pdf's. Our AI will assist you with all the pdf's information.")
user_question = st.text_input("Enter:", label_visibility="collapsed",
                                placeholder="Enter your question to receive answers from all uploaded pdfs.")


answer = ""
if user_question:

    question, answer, tokens = get_llm_answer(user_question=user_question)
   
    answer = answer
   
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "tokens_burned": tokens,
    })


if answer:
    st.subheader("✅ Answer")
    st.subheader(answer)

