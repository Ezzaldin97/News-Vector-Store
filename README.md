# News Vector Store

## Objective:
Large Language Models are designed to do human-language tasks effectively like Translation, Summarization, Reasoning, Classification, Capturing Contextual Information, Capture Semantics and Syntax of Languages, but recently after the emergance of GPT-3.5, and open-source Instruct models like Llama-2, Zephyer,..etc, we started to use LLMs in knowledge tasks like asking them about theories in Quantum Physics, Statistics, solving problems, debuging code, provide some information about specific domain use-cases, and more..
of course alot of them can provide answers to alot of questions, but once we starting asking them about questions LLMs don't know anything about or they can't memorize them, they hallucinate, and provide wrong answers.

a solution to this problem to use LLMs effectively, and provide them up to date information is by using Vector Databases & Prompt-Engineering Techniques to build Retrieval-Augmented Generation Systems, which can:

- Insert knowledge or context into the input.
- Ask the LM to incorporate the context in its output.

This Technique reduce hallucination, and provide LLMs with Context(Knowledge) they needs to answer questions effectively.

## Technologies & Prerequisites:

- python (>=3.10,<3.12)
- poetry
- basic knowledge in NLP & LLMs
- git & make command for Windows
- docker

## Project Setup:

- create two directories (db, news) in data directory
```bash
mkdir data/db
mkdir data/news
```
- create a directory (sts) and clone an encoder model from HuggingFace
that will encode your queries and data to embeddings,
i recommend using [model](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
```bash
mkdir sts
cd sts
git lfs install
git clone https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```
- create .env file to hold your secret keys.
- install dependancies
```bash
poetry install
``` 
- run the docker image of Qdrant DB API
```bash
make qdrant
```

## How it Works?

it is the simplest step just run this command
```bash
make run date='2023-11-09'
```

## Experiments:

- Query the Database and Search for News [Search](query_db.ipynb).
- Use OpenAI API and Extract News based on Questions [LLM-News-Reporter](llm_news_reporter.ipynb).