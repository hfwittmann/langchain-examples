"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""
import json
import time

import pandas as pd
import numpy as np
from langchain.chains import QAGenerationChain
from langchain.chat_models import ChatOpenAI
from langchain.evaluation import Criteria, EvaluatorType, load_evaluator
from langchain.llms import OpenAI, GPT4All
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def generate_questions(webdata, embeddings, user):
    start = time.time()

    # convert from jsons
    webdata_documents = [Document(**json.loads(d)) for d in webdata]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0
    )

    chain = QAGenerationChain.from_llm(
        llm=ChatOpenAI(temperature=0.0), text_splitter=text_splitter
    )

    QAs_long = chain.run(webdata_documents[0].page_content)

    k = 3
    QAs = QAs_long[:k]

    end = time.time()
    QAs_long.append({"time_taken": end - start})

    return (
        {
            "message": f"{len(QAs)} questions were generated for automatic evaluation purposes. The long version contains {len(QAs_long)-1}"
        },
        QAs,
        QAs_long,
    )


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
                    **subframe[["question", "result"]],
                }
            )
            D_new_llm.append(D_new)

        results_this_llm = pd.concat(D_new_llm)

        D.append(results_this_llm)

        if llm == llm_eval:
            reference_llm_eval = results_this_llm[["result"]]

    results = pd.concat(D, ignore_index=True)

    # start: add fake data
    # results2 = results.copy()
    # results2["llm"] = "FalconLLM"
    # results = pd.concat([results, results2], ignore_index=True)
    # stop : add fake data

    results["reference_llm_eval"] = np.resize(reference_llm_eval, len(results))
    # assign with recycling

    return results


def evaluate(QAs, criteria_list, llm_eval_name, llms, embeddings, models, user):
    llm_eval = OpenAI(temperature=0)

    falcon = models["falcon"]
    user = user
    user_local_path = eval(
        falcon["user_local_path"]
    )  # TODO Geht das auch besser?

    llm_eval = {
        "OpenAILLM": lambda: OpenAI(temperature=0),
        "FalconLLM": lambda: GPT4All(model=user_local_path, verbose=True),
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
            lambda row: _get_criteria_evaluation(
                evaluator=evaluator,
                input=row["question"],
                prediction=row["result"],
                reference=row["reference_llm_eval"],
            ),
            axis=1,
            result_type="expand",
        )
    return QAs
