"""
This is a boilerplate pipeline 'stepza_generate_questions_and_answers_pairs'
generated using Kedro 0.18.13
"""
import json
import logging
import time


from langchain.chains import QAGenerationChain
from langchain.chat_models import ChatOpenAI


from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def generate_questions_answers_pairs(webdata, k=3):
    start = time.time()

    # convert from jsons
    webdata_documents = [Document(**json.loads(d)) for d in webdata]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0
    )

    chain = QAGenerationChain.from_llm(
        llm=ChatOpenAI(temperature=0.0), text_splitter=text_splitter
    )

    QAs_long = chain.run(webdata_documents[0].page_content)

    QAs = QAs_long[:k]

    time_taken = time.time() - start

    logger.info(
        f"{len(QAs)} questions were generated for automatic evaluation purposes. The long version contains {len(QAs_long)}"
    )

    logging.info(f"time taken: {time_taken}")

    return (
        {
            "message": f"{len(QAs)} questions and answers were generated for automatic evaluation purposes. The long version contains {len(QAs_long)}"
        },
        QAs,
        QAs_long,
    )
