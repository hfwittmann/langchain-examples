"""
This is a boilerplate pipeline 'step04_retrieve'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import retrieve


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                retrieve,
                inputs=[
                    "embedding_message",
                    "params:questions",
                    "params:embedding",
                    "params:embeddings",
                    "params:models",
                ],
                outputs="docs_retrieved",
                name="retrieve",
                tags=["retrieve"],
            )
        ]
    )
