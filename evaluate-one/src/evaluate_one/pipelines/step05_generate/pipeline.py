"""
This is a boilerplate pipeline 'step05_generate'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import generate


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                generate,
                inputs=[
                    "docs_retrieved",
                    "params:questions",
                    "params:embedding",
                    "params:llm",
                    "params:embeddings",
                    "params:llms",
                    "params:models",
                ],
                outputs="generated_answer",
                name="generate",
                tags=["generate"],
            )
        ]
    )
