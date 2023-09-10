"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""
import json
import logging
import time

import numpy as np
import pandas as pd
from kedro.io import PartitionedDataSet
from langchain.chains import QAGenerationChain
from langchain.chat_models import ChatOpenAI
from langchain.evaluation import Criteria, EvaluatorType, load_evaluator
from langchain.llms import GPT4All, OpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)


def transform_questions_2_dataframe(QAs, llm_eval):
    D = list()

    QAs_filtered = {
        qa_key: qa_value
        for qa_key, qa_value in QAs.items()
        if "time_taken" not in qa_key
    }

    for llm, llm_value in QAs_filtered.items():
        D_new_llm = list()
        for embedding, llm_embedding_value in llm_value.items():
            subframe = pd.DataFrame(llm_embedding_value).T
            D_new = pd.DataFrame(
                {
                    "llm": llm,
                    "embedding": embedding,
                    **subframe[["question", "answer", "result"]],
                }
            )
            D_new_llm.append(D_new)

        results_this_llm = pd.concat(D_new_llm)

        D.append(results_this_llm)

    results = pd.concat(D, ignore_index=True)

    # start: add fake data
    # results2 = results.copy()
    # results2["llm"] = "FalconLLM"
    # results = pd.concat([results, results2], ignore_index=True)
    # stop : add fake data

    results["reference_llm_eval"] = results["answer"]
    # assign with recycling

    return results
