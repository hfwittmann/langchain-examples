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


def generate(docs_retrieved, questions, llms, embeddings, models, user):
    start = time.time()

    falcon = models["falcon"]
    user = user
    user_local_path = eval(falcon["user_local_path"])  # TODO Geht das auch besser?

    generated_answers = dict()
    docs_retrieved_docs = dict()

    for llm_name in llms["collections"]:
        generated_answers[llm_name] = {}

        llm = {
            "OpenAILLM": lambda: OpenAI(temperature=0),
            "FalconLLM": lambda: GPT4All(model=user_local_path, verbose=True),
        }[llm_name]

        chain = load_qa_chain(llm=llm(), chain_type="stuff")

        # convert from jsons
        for collection_name in embeddings["collections"]:
            generated_answers[llm_name][collection_name] = {}
            docs_retrieved_docs[collection_name] = {}

            for ix, q in enumerate(questions):
                ix = str(ix)
                generated_answers[llm_name][collection_name][ix] = {}
                docs_retrieved_docs[collection_name][ix] = {}

                # convert from jsons
                docs_retrieved_docs[collection_name][ix]["contexts"] = [
                    Document(**json.loads(d))
                    for d in docs_retrieved[collection_name][ix]["contexts"]
                ]
                # end : # convert from jsons

                start_llm_embedding = time.time()

                result = chain.run(
                    input_documents=docs_retrieved_docs[collection_name][ix][
                        "contexts"
                    ],
                    question=q["question"],
                )

                out = {
                    "llm_name": llm_name,
                    "question": q["question"],
                    "result": result,
                    "source_documents": docs_retrieved_docs[collection_name][ix][
                        "contexts"
                    ],
                }

                out["source_documents"] = [d.json() for d in out["source_documents"]]

                generated_answers[llm_name][collection_name][ix] = out

                end_llm_embedding = time.time()
                time_taken_llm_embedding = end_llm_embedding - start_llm_embedding
                generated_answers[llm_name][collection_name][ix][
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
