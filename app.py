
from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback



def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask Your PDF")

    #upload
    pdf = st.file_uploader("Upload your PDF here:")

    #extract text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text =  ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        #split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap = 200,
            length_function = len,
        )

        chunks = text_splitter.split_text(text)

        #embeddings
        embeddings = OpenAIEmbeddings()
        #FAISS - facebook ai similarity search
        knowlegde_base = FAISS.from_texts(chunks,embeddings)

        user_question = st.text_input("Ask you questions related to the pdf:")
        if user_question:
            docs = knowlegde_base.similarity_search(user_question)

            #langchain question answring
            
            llm=OpenAI()
            chain = load_qa_chain(llm,chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs,question=user_question)
                print(cb)

            st.write(response)




if __name__ == '__main__':
    main()