"""
This is a boilerplate pipeline 'step02_split'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import split, deduplicate


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                split,
                inputs="webdata_cleaned",
                outputs="split_webdata",
                name="split",
                tags=["split"],
            ),
            node(
                deduplicate,
                inputs=["split_webdata", "params:deduplicate"],
                outputs="webdata_deduplicated",
                name="deduplicate",
                tags=["deduplicate"],
            ),
        ]
    )
