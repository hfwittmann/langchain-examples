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


def evaluate(
    QAs_partitioned: PartitionedDataSet,
    _,
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
