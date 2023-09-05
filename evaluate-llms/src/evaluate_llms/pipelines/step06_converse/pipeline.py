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
                    "params:chat.llms",
                    "params:chat.embeddings",
                    "params:models",
                    "params:user",
                ],
                outputs="chat_result",
                name="converse",
                tags=["converse"],
            )
        ]
    )
