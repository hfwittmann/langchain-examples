"""
This is a boilerplate pipeline 'evaluate'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node, pipeline

from ..step04_retrieve.nodes import (
    retrieve as retrieve_contexts_automatic_questions,
)
from ..step05_generate.nodes import (
    generate as generate_answers_automatic_questions,
)
from .nodes import transform_questions_2_dataframe


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                retrieve_contexts_automatic_questions,
                inputs=[
                    "generated_questions_message",
                    "questions_answers_pairs_generated",
                    "params:embedding",
                    "params:embeddings",
                    "params:models",
                ],
                outputs="retrieve_contexts_automatic_questions",
                name="retrieve_contexts_automatic_questions",
                tags=["retrieve_contexts_automatic_questions"],
            ),
            node(
                generate_answers_automatic_questions,
                inputs=[
                    "retrieve_contexts_automatic_questions",
                    "questions_answers_pairs_generated",
                    "params:embedding",
                    "params:llm",
                    "params:embeddings",
                    "params:llms",
                    "params:models",
                ],
                outputs="generated_answers_automatic_questions",
                name="generate_answers_automatic_questions",
                tags=["generate_answers_automatic_questions"],
            ),
            node(
                transform_questions_2_dataframe,
                inputs=[
                    "generated_answers_automatic_questions",
                    "params:evaluation.llm_eval",
                ],
                outputs="generated_answers_automatic_questions_dataframe",
                name="transform_questions_2_dataframe",
                tags=["transform_questions_2_dataframe"],
            ),
        ]
    )
