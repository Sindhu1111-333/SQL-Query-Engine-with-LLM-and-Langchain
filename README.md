# SQL Query Engine with LLMs & LangChain

#Overview
This project builds an AI-powered SQL Query Engine using LangChain and LLMs (Large Language Models) to dynamically generate SQL queries from natural language prompts.

# Technologies Used
- OpenAI GPT-4 for natural language processing
- LangChain for structured query generation
- PostgreSQL for database interactions
- AdalFlow and LlamaIndex for enhancing data retrieval

Libraries
- [LangChain](https://github.com/langchain-ai/langchain)

## Getting Started

#Create an OpenAI Account: 
Sign up on [OpenAI](https://platform.openai.com/) and generate your API key.

#Setup Instructions:

Install PostgreSQL: This project uses [PostgreSQL](https://www.postgresql.org/download/macosx/).
    
Store the API Key : Set your OpenAI API key as an environment variable:
`export OPENAI_API_KEY=<your_api_key>`

Install Dependencies with UV:
To simplify the environment setup, install UV [Install](https://docs.astral.sh/uv/getting-started/installation/).

Run the command `uv sync` to install the python environment and all of the libraries under `.venv` folder.

You can also activate the environment manually: 
```sh
source .venv/bin/activate
```

PS: If you don't want to use uv, run
```sh
pip install .
```

#Database Setup
We'll be using Langchain to auto generate SQL queries based on tables.

- To load sample data, use dump file and restore it with:
 `pg_restore -h localhost -p 5432  -d postgres -U <your laptop username> data_dump.dump`

#running sql query engine
- Once everything is set up, you can run the query engine by executing:

python sql_llm.py

this will allow you to input natural language queries and get back generated SQL statements.

##Features

- Auto-generates SQL queries from natural language inputs.
- Supports multiple SQL databases (PostgreSQL, MySQL, etc.).


