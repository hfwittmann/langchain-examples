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
from collections import defaultdict


def generate(
    docs_retrieved, questions, embedding, llm, embeddings, llms, models
):
    start = time.time()
    assert isinstance(questions, list) and not isinstance(questions, str)

    assert llm in llms["collections"]
    assert embedding in embeddings["collections"]
    llm_name = llm
    collection_name = embedding

    llm_function = {
        "OpenAILLM": lambda: OpenAI(temperature=0),
        "FalconLLM": lambda: GPT4All(
            model=models["falcon"]["user_local_path"], verbose=True
        ),
    }[llm_name]

    chain = load_qa_chain(llm=llm_function(), chain_type="stuff")

    # convert from jsons
    # for collection_name in embeddings["collections"]:

    generated_answers = {}

    generated_answers = {}
    generated_answers[llm_name] = {}
    generated_answers[llm_name][collection_name] = {}

    for ix, q in enumerate(questions):
        ix = str(ix)

        docs_retrieved_docs = [
            Document(**json.loads(d))
            for d in docs_retrieved[collection_name][ix]["contexts"]
        ]

        result = chain.run(
            input_documents=docs_retrieved_docs,
            question=q["question"],
        )

        generated_answers[llm_name][collection_name][ix] = {
            "llm_name": llm_name,
            "question": q["question"],
            "result": result,
            "source_documents": docs_retrieved[collection_name][ix]["contexts"],
            "time_taken": time.time() - start,
        }

    # #######################################################################################

    return generated_answers
