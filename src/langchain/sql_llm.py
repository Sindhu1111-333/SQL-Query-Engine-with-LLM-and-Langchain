from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType
import os

# Load API Key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY', None)
if not API_KEY:
    raise ValueError("Error: Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI LLM for query processing
llm = OpenAI(temperature=0, openai_api_key=API_KEY, model_name='gpt-4')


# Function to create Gmail toolkit for email integration (Optional)
def create_gmail_toolkit():
    credentials = get_gmail_credentials(
        token_file="token.json",
        # Full Gmail access scope
        scopes=["https://mail.google.com/"],
        # Google API client secrets file
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    return GmailToolkit(api_resource=api_resource)


# Function to initialize Gmail agent
def create_gmail_agent(llm, toolkit):
    return initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )


# Set up Gmail Agent (Optional)
YOUR_EMAIL = '' # Set the email to receive results
agent = None
if YOUR_EMAIL:
    toolkit = create_gmail_toolkit()
    agent = create_gmail_agent(llm, toolkit)

# Load database connection URL from environment variable
database_url = os.getenv('LANGCHAIN_DATABASE_URL', None)
if not database_url:
    raise ValueError("Error: Please set the LANGCHAIN_DATABASE_URL environment variable.")

# Connect to PostgreSQL database(few tables included)
db = SQLDatabase.from_uri(
    database_url,
    include_tables=['medals', 'match_details', 'matches', 'medals_matches_players']
)

# Initialize SQLDatabaseChain for querying the database
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)


# --- FOR FIRST-TIME USERS ---
# The following query format is manually embedded for learning purposes.
# It is **commented out** because SQLDatabaseChain already handles query execution.

# QUERY = """
# Given an input question, first create a syntactically correct postgresql query to run, 
# then look at the results of the query and return the answer.
# Use the following format:
#
# Question: Question here
# SQLQuery: SQL Query to run
# SQLResult: Result of the SQLQuery
# Answer: Final answer here
#
# {question}
# """


def run_query(prompt):
    """Executes SQL query generated from natural language input."""
    try:
        # For first-time users who want to see the manual query structure:
        # question = QUERY.format(question=prompt)
        # results = db_chain.run(question)

        # Recommended approach (automatic query handling via LangChain)
        results = db_chain.run(prompt)

        if not results.strip():
            print("No results found for your query.")
            return

      """ #remove comment to see the SQL query that would be generated (for debugging purposes)
        print("Generated SQL Query:")
        print(db_chain.llm_chain.prompt.format(question=prompt))
      """

        print("Query Result:\n", results)

        if agent:
            email_content = f"Create an email with these results:\n\n{results}\n\nSend it to {YOUR_EMAIL} with the subject: '{prompt}'"
            agent.run(email_content)

    except Exception as e:
        print(f"Error processing query: {e}")


def get_prompt():
    """prompt to take user input and process SQL queries."""
    print("Type 'exit' to quit the program.")

    while True:
        prompt = input("Enter your SQL-related question: ").strip()

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        elif not prompt:
            print("Invalid input. Please enter a valid query.")
            continue
        else:
            run_query(prompt)


# Start interactive session to prompt the user
get_prompt()
