"""
This is a boilerplate pipeline 'step06_converse'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import evaluate_one


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                evaluate_one,
                inputs=[
                    "evaluation",
                    "params:embedding",
                    "params:llm",
                    "params:embeddings",
                    "params:llms",
                    "params:models",
                ],
                outputs=["evaluation_metrics", "evaluation_QAs_embedding_llm"],
                name="evaluate_one",
                tags=["evaluate_one"],
            )
        ]
    )
