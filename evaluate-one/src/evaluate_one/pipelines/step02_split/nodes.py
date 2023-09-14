"""
This is a boilerplate pipeline 'step02_split'
generated using Kedro 0.18.13
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json


def split(webdata):
    # convert from jsons
    webdata_documents = [Document(**d) for d in webdata]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0
    )

    all_splits = text_splitter.split_documents(webdata_documents)

    # convert to jsons
    all_splits_json = [d.json() for d in all_splits]

    return all_splits_json


def deduplicate(all_splits, deduplicate):
    if deduplicate:
        all_splits_deduplicated = list(set(all_splits))

    all_splits_deduplicated_jsons = [
        json.loads(d) for d in all_splits_deduplicated
    ]
    return all_splits_deduplicated_jsons
