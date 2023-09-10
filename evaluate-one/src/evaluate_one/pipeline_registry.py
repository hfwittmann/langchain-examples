"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline, pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())

    pipelines["get_webdata"] = pipeline(
        [
            p_value
            for p_key, p_value in pipelines.items()
            if p_key
            in [
                "step01_load",
                "step02_split",
            ]
        ]
    )

    pipelines["simple"] = pipeline(
        [
            p_value
            for p_key, p_value in pipelines.items()
            if p_key
            in [
                "step03_store",
                "step04_retrieve",
                "step05_generate",
            ]
        ]
    )

    pipelines["chat"] = pipeline(pipelines["step06_converse"])

    pipelines["generate_questions_and_answers_pairs"] = pipeline(
        pipelines["stepza_generate_questions_and_answers_pairs"]
    )

    pipelines["evaluate"] = pipeline(pipelines["stepzz_evaluate"])
    pipelines["evaluate_one"] = pipeline(pipelines["stepzz_evaluate_one"])

    return pipelines
