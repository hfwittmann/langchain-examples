"""
This is a boilerplate pipeline 'stepzz_evaluate_one'
generated using Kedro 0.18.13
"""
import json
from time import time
import logging
from kedro_mlflow.io.metrics import MlflowMetricsDataSet

logger = logging.getLogger(__name__)


def evaluate_one(QAs, embedding, llm, embeddings, llms, models):
    start = time()

    assert llm in llms["collections"]
    assert embedding in embeddings["collections"]
    # llm_name = llm
    # collection_name = embedding

    index = (QAs.embedding == embedding) & (QAs.llm == llm)

    QAs_embedding_llm = QAs[index]

    scores = [c for c in QAs.columns if "score" in c]
    values = [c for c in QAs.columns if "value" in c]
    reasoning = [c for c in QAs.columns if "reasoning" in c]

    metrics = QAs_embedding_llm[scores].mean()

    metrics_dict = dict(metrics)
    metrics_dict["total"] = metrics.mean()

    metrics_out = {
        key: {"value": value, "step": 0} for key, value in metrics_dict.items()
    }

    return metrics_out, QAs_embedding_llm
