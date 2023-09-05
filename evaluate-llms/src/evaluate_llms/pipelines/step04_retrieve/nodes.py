"""
This is a boilerplate pipeline 'step04_retrieve'
generated using Kedro 0.18.13
"""

from langchain.schema import Document
import json

from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb


def retrieve(message, questions, embeddings, models, user):
    assert isinstance(questions, list) and not isinstance(questions, str)

    persistent_client = chromadb.PersistentClient(embeddings["path"])

    sizes = dict()
    falcon = models["falcon"]
    user = user
    user_local_path = eval(falcon["user_local_path"])  # TODO Geht das auch besser?

    retrieved_documents = dict()

    for collection_name in embeddings["collections"]:
        embedding = {
            "OpenAIEmbeddings": OpenAIEmbeddings(),
            "FalconEmbeddings": GPT4AllEmbeddings(model=user_local_path),
        }[collection_name]

        retrieved_documents[collection_name] = dict()

        collection = persistent_client.get_or_create_collection(collection_name)

        langchain_chroma = Chroma(
            client=persistent_client,
            collection_name=collection_name,
            embedding_function=embedding,
        )

        assert collection.count() == langchain_chroma._collection.count()
        print("There are", langchain_chroma._collection.count(), "in the collection")

        for ix, q in enumerate(questions):
            ix = str(ix)
            docs_retrieved = langchain_chroma.similarity_search(q["question"])

            # convert to jsons
            docs_retrieved_json = [d.json() for d in docs_retrieved]

            retrieved_documents[collection_name][ix] = dict()
            retrieved_documents[collection_name][ix]["question"] = q["question"]
            retrieved_documents[collection_name][ix]["contexts"] = docs_retrieved_json

    return retrieved_documents
