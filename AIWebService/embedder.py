# FOR OPENAI EMBEDDINGS AND VECTOR DB SEARCHING
# STEPS TO GET OPENAI CONTEXTS:
# 1. Get the intent and entities from the query
# 2. Embed relevant documents
# 3. Get the top 5 most similar documents

from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.callbacks import get_openai_callback
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
from dotenv import load_dotenv

load_dotenv()
import os
import openai
import re

# add OPENAI_API_KEY as an env

def get_vector_results(query, pdf='teach_spinny.pdf'):
    print('Searching for ', query)
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text().replace('\n', ' ')
    # print(text)

    #split into questions and answers pairings
    qa_pairs = []
    pattern = r'Question: (.*?)(?: Answer: (.*?)(?= Question:|$))'
    matches = re.findall(pattern, text, re.DOTALL)
    for question, answer in matches:
        qa_pairs.append({'question': question, 'answer': answer})

    # combine into a question and answer pair list for embedding
    qa_list = [(qa_pairs['question'] + qa_pairs['answer']) for qa_pairs in qa_pairs]

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=500,
    #     chunk_overlap=150,
    #     length_function=len
    #     )
    # chunks = text_splitter.split_text(text=text)

    # # embeddings
    store_name = pdf[:-4]
    print(f'{store_name}')
    # st.write(chunks)

    if os.path.exists(f"{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
        print('Embeddings Loaded from the Disk')
    else:
        print('Making new path')
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(qa_list, embedding=embeddings)
        with open(f"{store_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(qa_list, embedding=embeddings)

    # query = input("Ask questions about your PDF file:")
    docs = VectorStore.similarity_search(query=query, k=2)
    # print docs[0] 's text
    # print(f"DOCS 0 :{docs[0].page_content}")
    results = f"""****** FROM 'S DOCUMENTATION - results generated through vector searching of keyword:\n\n****RESULT 1: ...{docs[0].page_content}... \n\n****RESULT 2: ...{docs[1].page_content}... \n\n"""
    return results



# print(get_vector_results('whats s data sharing policy', 'teach_spinny.pdf'))