"""
This is a boilerplate pipeline 'step03_store'
generated using Kedro 0.18.13
"""
from langchain.schema import Document
import json

from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb
import ast


def store(split_webdata, embeddings, user):
    # llm = GPT4All(model=local_path, verbose=True)
    # embedding =

    # convert from jsons
    split_webdata_documents = [Document(**json.loads(d)) for d in split_webdata]

    persistent_client = chromadb.PersistentClient(embeddings["path"])

    sizes = dict()
    falcon = embeddings["falcon"]

    user_local_path = eval(
        falcon["user_local_path"]
    )  # TODO Geht das auch besser?

    for collection_name in embeddings["collections"]:
        embedding = {
            "OpenAIEmbeddings": OpenAIEmbeddings(),
            "FalconEmbeddings": GPT4AllEmbeddings(model=user_local_path),
        }[collection_name]

        vectorstore = Chroma.from_documents(
            documents=split_webdata_documents,
            embedding=embedding,
            collection_name=collection_name,
            client=persistent_client,
        )

        sizes[collection_name] = vectorstore._collection.count()

    return {
        "message": f"embeddings for the collections {embeddings['collections']} have been saved",
        "collection_sizes": sizes,
    }
