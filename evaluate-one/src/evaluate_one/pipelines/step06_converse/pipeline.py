"""
This is a boilerplate pipeline 'step06_converse'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import converse


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                converse,
                inputs=[
                    "params:chat.questions",
                    "params:embedding",
                    "params:llm",
                    "params:embeddings",
                    "params:llms",
                    "params:models",
                ],
                outputs="chat_result",
                name="converse",
                tags=["converse"],
            )
        ]
    )
