"""
This is a boilerplate pipeline 'step06_converse'
generated using Kedro 0.18.13
"""
"""
This is a boilerplate pipeline 'step06_converse'
generated using Kedro 0.18.13
"""

import json
import time

import chromadb
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.llms import GPT4All, OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma


def converse(chat_questions, embedding, llm, embeddings, llms, models):
    start = time.time()
    assert isinstance(chat_questions, list) and not isinstance(
        chat_questions, str
    )

    assert llm in llms["collections"]
    assert embedding in embeddings["collections"]
    llm_name = llm
    collection_name = embedding

    persistent_client = chromadb.PersistentClient(embeddings["path"])

    llm_function = {
        "OpenAILLM": lambda: OpenAI(temperature=0),
        "FalconLLM": lambda: GPT4All(
            model=models["falcon"]["user_local_path"], verbose=True
        ),
        "Orca3LLM": lambda: GPT4All(
            model=models["orca_3"]["user_local_path"], verbose=True
        ),
        "Orca7LLM": lambda: GPT4All(
            model=models["orca_7"]["user_local_path"], verbose=True
        ),
        "Orca13LLM": lambda: GPT4All(
            model=models["orca_13"]["user_local_path"], verbose=True
        ),
    }[llm_name]

    embedding = {
        "OpenAIEmbeddings": OpenAIEmbeddings(),
        "GPT4AllEmbeddings": GPT4AllEmbeddings(),
    }[collection_name]

    # collection = persistent_client.get_or_create_collection("myopenai")
    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedding,
    )

    # expose this index in a retriever interface
    retriever = langchain_chroma.as_retriever()

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )
    this_chat = ConversationalRetrievalChain.from_llm(
        llm_function(), retriever=retriever, memory=memory
    )

    for q in chat_questions:
        result = this_chat({"question": q["question"]})

    # convert to jsons
    result["chat_history"] = [d.json() for d in result["chat_history"]]

    out = {
        llm_name: {
            collection_name: {
                "result": result,
                "time_taken": time.time() - start,
            }
        }
    }

    return out
