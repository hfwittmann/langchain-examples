from __future__ import annotations
from pathlib import PurePosixPath
from posixpath import split
from typing import Any, Dict

import json

import fsspec
import pandas as pd


from langchain.schema import Document
import json
from typing import Iterable

from kedro.io import AbstractDataSet
from kedro.io.core import get_filepath_str, get_protocol_and_path


class LangchainDataSet(AbstractDataSet):
    """``HuggingfaceDataSet`` loads / save image data from a given filepath as `numpy` array using Pillow.

    Example:
    ::

        >>> HuggingfaceDataSet(filepath='/img/file/path')
    """

    def __init__(self, filepath: str, subtype: str):
        """Creates a new instance of HuggingfaceDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)
        self._subtype = subtype

    # https://github.com/langchain-ai/langchain/issues/3016
    def _load(self) -> Iterable[Document]:
        """Loads data from the specified filepath

        Returns:
            Data from  file
        """
        file_path = get_filepath_str(self._filepath, self._protocol)

        array = []
        with open(file_path, "r") as jsonl_file:
            for line in jsonl_file:
                data = json.loads(line)
                obj = Document(**data)
                array.append(obj)
        return array

    def _save(self, dataset_list: list[Document]) -> None:
        """Saves data to the specified filepath."""

        file_path = get_filepath_str(self._filepath, self._protocol)
        with open(file_path, "w") as jsonl_file:
            for doc in dataset_list:
                jsonl_file.write(doc.json() + "\n")

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset."""
        return dict(filepath=self._filepath, protocol=self._protocol)
