import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .parser import AnswerResponse
import chromadb
from langchain_community.callbacks import get_openai_callback

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPEN_AI_KEY')

embeddings_model = OpenAIEmbeddings(api_key=API_KEY)
llm_model = ChatOpenAI(api_key=API_KEY)
persistent_client = chromadb.PersistentClient()

vector_store_from_client = Chroma(
    collection_name="resumes_embeddings",
    embedding_function=embeddings_model,
    client=persistent_client,

)


def upload_to_vectors_db(save_path):
    loader = PyPDFLoader(save_path)
    pages = loader.load()

    os.remove(save_path)

    documents = []
    documents_ids = []
    for page in pages:
        documents.append(page)
        documents_ids.append(
            str(f"{page.metadata['source']}_{page.metadata['page']}"))

    existed = vector_store_from_client.get(ids=documents_ids)

    if not existed['ids']:
        vector_store_from_client.add_documents(
            documents=documents, ids=documents_ids)


def get_llm_answer(user_question):
    retriever = vector_store_from_client.as_retriever()

    system_prompt = """
        You are an assistant tasked with answering questions. Follow these conditions:
        1. Use the provided context to answer the question.
        2. Keep the answer short in 2 lines.
        3. If you don't know the answer, clearly state that you don't know.
        4. Provide the response in JSON format with the keys: "question", "answer", and "date".
        
        {context}
        """

    parser = JsonOutputParser(pydantic_object=AnswerResponse)
    prompt = ChatPromptTemplate(
        messages=[
            ("system", system_prompt),
            ("human", "{input}"),
        ],
        output_parser=parser,
        partial_variables={
            "format_instructions": parser.get_format_instructions()},
    )

    question_answer_chain = create_stuff_documents_chain(llm_model, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    with get_openai_callback() as cb:
        results = rag_chain.invoke({"input": user_question})

        total_tokens = cb.total_tokens

        response = parser.parse(results['answer'])
    return response['question'], response['answer'], total_tokens
