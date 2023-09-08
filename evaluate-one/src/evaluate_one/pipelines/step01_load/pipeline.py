"""
This is a boilerplate pipeline 'step01_load'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import load


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                load,
                inputs="params:url",
                outputs="webdata",
                name="load",
                tags=["load"],
            )
        ]
    )
