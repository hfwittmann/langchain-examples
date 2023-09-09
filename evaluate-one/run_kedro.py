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

for embedding in tqdm(embeddings):
    for llm in tqdm(llms):
        with KedroSession.create(
            extra_params={"embedding": embedding, "llm": llm}
        ) as session:
            session.run(pipeline_name="evaluate")


# with KedroSession.create(
#     extra_params={"embedding": "FalconEmbeddings", "llm": "FalconLLM"}
# ) as session:
#     session.run()
