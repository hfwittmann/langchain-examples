"""
This is a boilerplate pipeline 'step04_retrieve'
generated using Kedro 0.18.13
"""

from langchain.schema import Document
import json

from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb
import logging

logger = logging.getLogger(__name__)


def retrieve(_, questions, embedding, embeddings, models):
    assert isinstance(questions, list) and not isinstance(questions, str)

    assert embedding in embeddings["collections"]
    collection_name = embedding

    persistent_client = chromadb.PersistentClient(embeddings["path"])

    sizes = dict()

    retrieved_documents = dict()

    embedding_function = {
        "OpenAIEmbeddings": OpenAIEmbeddings(),
        "FalconEmbeddings": GPT4AllEmbeddings(
            model=models["falcon"]["user_local_path"]
        ),
        "Orca3Embeddings": GPT4AllEmbeddings(
            model=models["orca_3"]["user_local_path"]
        ),
        "Orca7Embeddings": GPT4AllEmbeddings(
            model=models["orca_7"]["user_local_path"]
        ),
        "Orca13Embeddings": GPT4AllEmbeddings(
            model=models["orca_13"]["user_local_path"]
        ),
    }[collection_name]

    retrieved_documents[collection_name] = dict()

    collection = persistent_client.get_or_create_collection(collection_name)

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )

    assert collection.count() == langchain_chroma._collection.count()
    logger.info(
        f"There are {langchain_chroma._collection.count()}in the collection"
    )

    for ix, q in enumerate(questions):
        ix = str(ix)
        docs_retrieved = langchain_chroma.similarity_search(q["question"])

        # convert to jsons
        docs_retrieved_json = [d.json() for d in docs_retrieved]

        retrieved_documents[collection_name][ix] = dict()
        retrieved_documents[collection_name][ix]["question"] = q["question"]
        retrieved_documents[collection_name][ix][
            "contexts"
        ] = docs_retrieved_json

    return retrieved_documents
