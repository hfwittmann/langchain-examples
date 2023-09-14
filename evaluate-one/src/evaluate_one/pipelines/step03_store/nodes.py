"""
This is a boilerplate pipeline 'step03_store'
generated using Kedro 0.18.13
"""
from langchain.schema import Document
import json

from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb
import logging

logger = logging.getLogger(__name__)


def store(split_webdata, embedding, embeddings, models):
    assert embedding in embeddings["collections"]
    collection_name = embedding

    # convert from jsons
    split_webdata_documents = [Document(**json.loads(d)) for d in split_webdata]
    persistent_client = chromadb.PersistentClient(embeddings["path"])

    embedding_function = {
        "OpenAIEmbeddings": OpenAIEmbeddings(),
        "GPT4AllEmbeddings": GPT4AllEmbeddings(),
    }[collection_name]

    vectorstore = Chroma(
        collection_name=collection_name,
        client=persistent_client,
    )

    size = vectorstore._collection.count()
    if size > 0:
        # embeddings found in collection
        logger.info(
            f"embeddings for the collection {collection_name} have been found, therefore no new embeddings were saved"
        )

    elif size == 0:
        # no embeddings found in collection
        vectorstore = Chroma.from_documents(
            documents=split_webdata_documents,
            embedding=embedding_function,
            collection_name=collection_name,
            client=persistent_client,
        )

        size = vectorstore._collection.count()

        logger.info(
            f"embeddings for the collection {collection_name} have been saved"
        )

    return {
        "message": f"There are {size} embeddings  in the collection {collection_name}"
    }
