from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path
from tqdm import tqdm

# If you are creating a session outside of a Kedro project (i.e. not using
# `kedro run` or `kedro jupyter`), you need to run `bootstrap_project` to
# let Kedro find your configuration.
bootstrap_project(
    Path(
        "/home/hfwittmann/Sync/DataScience/mylangchain/langchain-examples/evaluate-one"
    )
)

# with KedroSession.create() as session:
#     context = session.load_context()

#     try:
#         blub = context.catalog.load("questions_answers_pairs_generated")
#     except Exception as e:
#         pass

#     pass


embeddings = ["OpenAIEmbeddings", "FalconEmbeddings"]
llms = ["OpenAILLM", "FalconLLM"]

combinations = [
    (embedding, llm) for embedding in tqdm(embeddings) for llm in tqdm(llms)
]
# combinations are ordered (embedding, llm) pairs

# with KedroSession.create() as session:
#     session.run(pipeline_name="get_webdata")

# for pipeline_name in tqdm(["simple", "chat"]):
#     print(f"Running pipeline: {pipeline_name}")
#     for embedding, llm in tqdm(combinations):
#         with KedroSession.create(
#             extra_params={"embedding": embedding, "llm": llm}
#         ) as session:
#             session.run(pipeline_name=pipeline_name)

# with KedroSession.create() as session:
#     session.run(pipeline_name="generate_questions_and_answers_pairs")

# for pipeline_name in tqdm(["stepzb_generate_results"]):
#     print(f"Running pipeline: {pipeline_name}")
#     for embedding, llm in tqdm(combinations):
#         with KedroSession.create(
#             extra_params={"embedding": embedding, "llm": llm}
#         ) as session:
#             session.run(pipeline_name=pipeline_name)


# for pipeline_name in tqdm(["evaluate"]):
#     print(f"Running pipeline: {pipeline_name}")
#     with KedroSession.create() as session:
#         session.run(pipeline_name=pipeline_name)

for pipeline_name in tqdm(["stepzz_evaluate_one"]):
    print(f"Running pipeline: {pipeline_name}")
    for embedding, llm in tqdm(combinations):
        with KedroSession.create(
            extra_params={"embedding": embedding, "llm": llm}
        ) as session:
            session.run(pipeline_name=pipeline_name)
