from vanna.base import VannaBase
from vanna.groq.groq import Groq    
from vanna.pgvector.pgvector import PG_VectorStore

import warnings
warnings.filterwarnings("ignore")

class MyVanna(PG_VectorStore, Groq):
    def __init__(self, config=None):
        if config is None:
            config = {}

        connection_string = config.get("connection_string", "postgresql+psycopg://postgres:test@localhost:5432/uni2")

        PG_VectorStore.__init__(self, config={"connection_string": connection_string})

        api_key=config.get("api_key","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")
        model=config.get("model","llama-3.1-70b-versatile")

        Groq.__init__(self,
                      config={"api_key":api_key,"model":model,"temperature":0.1,"top_k":50}
                      
                     )

vn = MyVanna()

import streamlit as st

# Simulating a function to convert a question into SQL query
def generate_sql(query):
    # In practice, you would replace this with your logic
    # to map the question to a SQL query.
    #return f"SELECT * FROM table WHERE column LIKE '%{query}%'"
    return vn.generate_sql(question)

# Streamlit UI
st.title("Question to SQL Generator")

# Input field for user's question
question = st.text_input("Enter your question")

# Generate SQL button
if st.button("Generate SQL"):
    if question:
        sql_query = generate_sql(question)
        st.code(sql_query, language='sql')

        # Adding the Copy to Clipboard button
        st.text_area("Copy the SQL query", value=sql_query, height=100)
        st.write("Press Ctrl+C / Cmd+C to copy the query after selecting it.")

        #st.write(f"Generated SQL Query: `{sql_query}`")
    else:
        st.error("Please enter a question.")
