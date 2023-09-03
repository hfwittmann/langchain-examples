"""
This is a boilerplate pipeline 'step05_generate'
generated using Kedro 0.18.13
"""
import json
import time

import chromadb
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import GPT4All, OpenAI
from langchain.schema import Document
from langchain.vectorstores import Chroma


def generate(docs_retrieved, question, llms, embeddings, models, user):
    start = time.time()

    falcon = models["falcon"]
    user = user
    user_local_path = eval(falcon["user_local_path"])  # TODO Geht das auch besser?

    generated_answers = dict()
    docs_retrieved_docs = dict()

    # convert from jsons
    for collection_name in embeddings["collections"]:
        docs_retrieved_docs[collection_name] = [
            Document(**json.loads(d)) for d in docs_retrieved[collection_name]
        ]
    # end : # convert from jsons

    for llm_name in llms["collections"]:
        llm = {
            "OpenAILLM": lambda: OpenAI(temperature=0),
            "FalconLLM": lambda: GPT4All(model=user_local_path, verbose=True),
        }[llm_name]

        chain = load_qa_chain(llm=llm(), chain_type="stuff")
        query = question

        generated_answers[llm_name] = {}

        # convert from jsons
        for collection_name in embeddings["collections"]:
            start_llm_embedding = time.time()
            generated_answers[llm_name][collection_name] = {}

            result = chain.run(
                input_documents=docs_retrieved_docs[collection_name], question=query
            )

            out = {
                "llm_name": llm_name,
                "query": query,
                "result": result,
                "source_documents": docs_retrieved_docs[collection_name],
            }

            out["source_documents"] = [d.json() for d in out["source_documents"]]

            generated_answers[llm_name][collection_name] = out

            end_llm_embedding = time.time()
            time_taken_llm_embedding = end_llm_embedding - start_llm_embedding
            generated_answers[llm_name][collection_name][
                "time_taken_llm_embedding"
            ] = time_taken_llm_embedding

    # #######################################################################################

    # persistent_client = chromadb.PersistentClient("data/03_primary/openai_embeddings")
    # collection = persistent_client.get_or_create_collection("myopenai")
    # langchain_chroma = Chroma(
    #     client=persistent_client,
    #     collection_name="myopenai",
    #     embedding_function=OpenAIEmbeddings(),
    # )

    # # expose this index in a retriever interface
    # retriever = langchain_chroma.as_retriever(
    #     search_type="similarity", search_kwargs={"k": 4}
    # )

    # # create a chain to answer questions
    # qa = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=retriever,
    #     return_source_documents=True,
    # )
    # query = "Who is Bernhard Kube?"
    # out2 = qa({"query": query})

    # assert out["result"] == out2["result"]

    # convert to jsons
    end = time.time()
    generated_answers["time_taken"] = end - start

    return generated_answers
