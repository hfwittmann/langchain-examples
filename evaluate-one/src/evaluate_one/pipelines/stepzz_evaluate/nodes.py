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


def evaluate(
    QAs_partitioned: PartitionedDataSet,
    criteria_list,
    llm_eval_name,
    llms,
    models,
):
    QAs = pd.DataFrame()

    for partition_key, partition_load_func in sorted(QAs_partitioned.items()):
        partition_data = partition_load_func()  # load the actual partition data
        # concat with existing result
        QAs = pd.concat([QAs, partition_data], ignore_index=True, sort=True)

    assert llm_eval_name in llms["collections"]
    llm_eval = {
        "OpenAILLM": lambda: OpenAI(temperature=0),
        "FalconLLM": lambda: GPT4All(
            model=models["falcon"]["user_local_path"], verbose=True
        ),
        "Orca3LLM": lambda: GPT4All(
            model=models["orca_3"]["user_local_path"], verbose=True
        ),
        "Orca7LLM": lambda: GPT4All(
            model=models["orca_7"]["user_local_path"], verbose=True
        ),
        "Orca13LLM": lambda: GPT4All(
            model=models["orca_13"]["user_local_path"], verbose=True
        ),
    }[llm_eval_name]

    def _get_criteria_evaluation(evaluator, input, prediction, reference):
        eval_result = evaluator.evaluate_strings(
            input=input,
            prediction=prediction,
            reference=reference,
        )

        return [
            eval_result["reasoning"],
            eval_result["value"],
            eval_result["score"],
        ]

    for (
        criteria
    ) in criteria_list:  # ["correctness", "helpfulness", "relevance"]:
        evaluator = load_evaluator(
            EvaluatorType.LABELED_CRITERIA, llm=llm_eval(), criteria=criteria
        )

        QAs[
            [
                f"{criteria}_reasoning",
                f"{criteria}_value",
                f"{criteria}_score",
            ]
        ] = QAs.apply(
            lambda row, evaluator=evaluator: _get_criteria_evaluation(
                evaluator=evaluator,
                input=row["question"],
                prediction=row["result"],
                reference=row["reference_llm_eval"],
            ),
            axis=1,
            result_type="expand",
        )
    return QAs
