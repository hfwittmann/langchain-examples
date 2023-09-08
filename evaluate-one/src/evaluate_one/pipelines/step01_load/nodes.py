"""
This is a boilerplate pipeline 'step01_load'
generated using Kedro 0.18.13
"""

# from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup


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
