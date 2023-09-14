"""
This is a boilerplate pipeline 'step01_load'
generated using Kedro 0.18.13
"""

import json
import re

from bs4 import BeautifulSoup as Soup

# from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader


def load(url):
    # simpler loader
    # loader = WebBaseLoader("https://www.lufthansa-industry-solutions.com/de-en/")

    loader = RecursiveUrlLoader(
        url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text
    )
    data = loader.load()

    # convert to jsons
    data_jsons = [d.json() for d in data]

    return data_jsons


def clean(webdata, clean_reg_ex):
    webdata_jsons = [json.loads(d) for d in webdata]

    for d_j in webdata_jsons:
        for match in clean_reg_ex:
            pattern, repl = match["pattern"], match["repl"]
            d_j["page_content"] = re.sub(
                pattern=pattern, repl=repl, string=d_j["page_content"]
            )

    return webdata_jsons
