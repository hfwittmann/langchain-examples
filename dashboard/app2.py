import gradio as gr
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import GPT4All
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import logging
from langchain.chains.question_answering import load_qa_chain
import chromadb
from langchain import PromptTemplate

logger = logging.getLogger(__name__)


llm_function = GPT4All(
    model="ggml-model-gpt4all-falcon-q4_0.bin",
    allow_download=False,
)
embedding = GPT4AllEmbeddings()

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in German:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def get_text_chunks_langchain(text):
    assert isinstance(text, list) and not isinstance(text, str)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.create_documents(text)
    return all_splits


def generate_text(question, background_text):
    all_splits = get_text_chunks_langchain([background_text])

    collection_name = "current"

    client = chromadb.EphemeralClient()

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        client=client,
    )
    size = vectorstore._collection.count()

    logger.info(f"{size} embeddings were found")

    if size > 0:
        # embeddings found in collection
        logger.info(
            f"embeddings for the collection {collection_name} have been found, therefore no new embeddings were saved"
        )

    elif size == 0:
        # no embeddings found in collection
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=embedding,
            collection_name=collection_name,
            client=client,
        )

        size = vectorstore._collection.count()

        logger.info(f"embeddings for the collection {collection_name} have been saved")

    assert len(all_splits) == size, f"{len(all_splits)} and {size} should be equal"

    docs_retrieved = vectorstore.similarity_search(question, k=4)

    chain = load_qa_chain(llm=llm_function, chain_type="stuff", prompt=PROMPT)

    # result = chain.run(
    #     input_documents=docs_retrieved,
    #     question=prompt,
    # )

    result = chain({"input_documents": docs_retrieved, "question": question})

    # convert to jsons
    docs_retrieved_json = [d.json() for d in docs_retrieved]

    return result, docs_retrieved_json


demo = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.components.Textbox(label="Frage"),
        gr.components.Textbox(label="Background Text"),
    ],
    outputs=[
        gr.components.Textbox(label="Generated Text"),
        gr.Dropdown(label="Identified snippets"),
    ],
    title="Falcon-7B Instruct",
)

if __name__ == "__main__":
    demo.launch(share=True, server_port=7860, server_name="0.0.0.0")
