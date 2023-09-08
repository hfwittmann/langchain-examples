from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path

# If you are creating a session outside of a Kedro project (i.e. not using
# `kedro run` or `kedro jupyter`), you need to run `bootstrap_project` to
# let Kedro find your configuration.
bootstrap_project(
    Path(
        "/home/hfwittmann/Sync/DataScience/mylangchain/langchain-examples/evaluate-one"
    )
)

embeddings = ["OpenAIEmbeddings", "FalconEmbeddings"]
llms = ["OpenAILLM", "FalconLLM"]


for embedding in embeddings:
    for llm in llms:
        with KedroSession.create(
            extra_params={"embedding": embedding, "llm": llm}
        ) as session:
            session.run()


# with KedroSession.create(
#     extra_params={"embedding": "FalconEmbeddings", "llm": "FalconLLM"}
# ) as session:
#     session.run()
