"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    generate_questions_answers_pairs,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                generate_questions_answers_pairs,
                inputs=[
                    "webdata",
                ],
                outputs=[
                    "generated_questions_message",
                    "questions_answers_pairs_generated",
                    "questions_answers_pairs_generated_long",
                ],
                name="generate_questions_answers_pairs",
                tags=["generate_questions_answers_pairs"],
            ),
        ]
    )
