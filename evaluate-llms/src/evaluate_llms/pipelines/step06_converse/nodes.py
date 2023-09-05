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


def converse(questions, llms, embeddings, models, user):
    start = time.time()
    persistent_client = chromadb.PersistentClient(embeddings["path"])

    falcon = models["falcon"]
    user = user
    user_local_path = eval(falcon["user_local_path"])  # TODO Geht das auch besser?

    out = {}

    for llm_name in llms["collections"]:
        llm = {
            "OpenAILLM": lambda: OpenAI(temperature=0),
            "FalconLLM": lambda: GPT4All(model=user_local_path, verbose=True),
        }[llm_name]

        chain = load_qa_chain(llm=llm(), chain_type="stuff")

        out[llm_name] = {}

        # convert from jsons
        for collection_name in embeddings["collections"]:
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )

            start_llm_embedding = time.time()
            out[llm_name][collection_name] = {}

            embedding = {
                "OpenAIEmbeddings": OpenAIEmbeddings(),
                "FalconEmbeddings": GPT4AllEmbeddings(model=user_local_path),
            }[collection_name]

            # collection = persistent_client.get_or_create_collection("myopenai")
            langchain_chroma = Chroma(
                client=persistent_client,
                collection_name=collection_name,
                embedding_function=embedding,
            )

            # expose this index in a retriever interface
            retriever = langchain_chroma.as_retriever()
            this_chat = ConversationalRetrievalChain.from_llm(
                llm(), retriever=retriever, memory=memory
            )

            for q in questions:
                result = this_chat({"question": q["question"]})

            # convert to jsons
            result["chat_history"] = [d.json() for d in result["chat_history"]]

            out[llm_name][collection_name]["result"] = result

            end_llm_embedding = time.time()
            time_taken_llm_embedding = end_llm_embedding - start_llm_embedding
            out[llm_name][collection_name][
                "time_taken_llm_embedding"
            ] = time_taken_llm_embedding

    end = time.time()
    out["time_taken"] = end - start

    return out
