"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                evaluate,
                inputs=[
                    "generated_answers_automatic_questions_dataframe_all",
                    "params:evaluation.criteria_list",
                    "params:evaluation.llm_eval",
                    "params:evaluation.llms",
                    "params:models",
                ],
                outputs="evaluation",
                name="evaluate",
                tags=["evaluate"],
            ),
        ]
    )
