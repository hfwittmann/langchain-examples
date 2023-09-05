"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""
import json
import time

import pandas as pd
from langchain.chains import QAGenerationChain
from langchain.chat_models import ChatOpenAI
from langchain.evaluation import Criteria, EvaluatorType, load_evaluator
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def generate_questions(webdata, embeddings, user):
    start = time.time()

    # convert from jsons
    webdata_documents = [Document(**json.loads(d)) for d in webdata]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

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


def evaluate(QAs, criteria, llms, embeddings, models, user):
    QAs_filtered = {
        qa_key: qa_value
        for qa_key, qa_value in QAs.items()
        if "time_taken" not in qa_key
    }

    D = list()

    for llm, llm_value in QAs_filtered.items():
        for embedding, llm_embedding_value in llm_value.items():
            subframe = pd.DataFrame(llm_embedding_value).T
            D_new = pd.DataFrame(
                {"llm": llm, "embedding": embedding, **subframe[["question", "result"]]}
            )
            D.append(D_new)

    results = pd.concat(D)

    llm_eval = OpenAI(temperature=0)
    evaluator = load_evaluator(
        EvaluatorType.LABELED_CRITERIA, llm=llm_eval, criteria="helpfulness"
    )

    def _get_criteria_evaluation(evaluator, input, prediction, reference):
        eval_result = evaluator.evaluate_strings(
            input=input,
            prediction=prediction,
            reference=reference,
        )

        return [eval_result["reasoning"], eval_result["value"], eval_result["score"]]

    for criteria in ["correctness", "helpfulness", "relevance"]:
        evaluator = load_evaluator(
            EvaluatorType.LABELED_CRITERIA, llm=llm_eval, criteria=criteria
        )

    results
