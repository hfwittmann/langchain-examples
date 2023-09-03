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
                    "embeddings_message",
                    "params:question",
                    "params:embeddings",
                    "params:models",
                    "params:user",
                ],
                outputs="docs_retrieved",
                name="retrieve",
                tags=["retrieve"],
            )
        ]
    )
