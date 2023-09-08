"""
This is a boilerplate pipeline 'step03_store'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import store


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                store,
                inputs=[
                    "split_webdata",
                    "params:embedding",
                    "params:embeddings",
                    "params:models",
                ],
                outputs="embedding_message",
                name="store",
                tags=["store"],
            )
        ]
    )
