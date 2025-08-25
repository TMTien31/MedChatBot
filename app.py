from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

embeddings = download_hugging_face_embeddings()


index_name = "medchatbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.4,
    max_output_tokens=4069
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
# legacy chain
# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

translate_vi_to_en_chain = translate_vi_to_en_prompt | llm | StrOutputParser()
translate_en_to_vi_chain = translate_en_to_vi_prompt | llm | StrOutputParser()

rag_chain = (
    RunnableLambda(lambda x: translate_vi_to_en_chain.invoke({"text": x["text"]}))
    | RunnableLambda(lambda x: {"input": x})
    | {
        "context": lambda x: retriever.invoke(x["input"]),
        "input": itemgetter("input"),
    }
    | prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda x: translate_en_to_vi_chain.invoke({"text": x}))
)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"text": msg})
    print("Response : ", response)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)