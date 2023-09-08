"""
This is a boilerplate pipeline 'step02_split'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import split


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                split,
                inputs="webdata",
                outputs="split_webdata",
                name="split",
                tags=["split"],
            )
        ]
    )
