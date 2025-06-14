import streamlit as st
import sqlite3
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(page_title="AI HR Database Tool", page_icon="📊")
st.title("📊 Ask Your HR Database")
st.caption("Ask in plain English (e.g., 'Show average salary by department')")

# Detect current table and schema
def get_schema():
    with sqlite3.connect("hr.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        if not tables:
            return ""
        table = tables[0][0]
        cur.execute(f"PRAGMA table_info({table})")
        columns = cur.fetchall()
        col_names = [col[1] for col in columns]
        return f"Table: {table}({', '.join(col_names)})"

# Convert question to SQL
def generate_sql(question, schema):
    prompt = f"""
You are an expert SQL assistant. Convert this natural language question into a valid SQLite SQL query.
Return ONLY the SQL query. No explanation. No formatting.

Question: {question}
{schema}
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Execute SQL
def execute_sql(query):
    with sqlite3.connect("hr.db") as conn:
        cur = conn.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return rows, columns
        except Exception as e:
            return str(e), []

# Text input
question = st.text_input("Ask a question:")

# Run logic
if question:
    schema = get_schema()
    if not schema:
        st.warning("⚠️ Please upload a CSV first.")
    else:
        with st.spinner("Thinking..."):
            sql = generate_sql(question, schema)
            st.subheader("💡 Generated SQL")
            st.code(sql, language="sql")
            result, cols = execute_sql(sql)

        if isinstance(result, str):
            st.error(f"❌ SQL Error: {result}")
        elif result:
            st.success("✅ Result:")
            st.dataframe([dict(zip(cols, row)) for row in result])
        else:
            st.warning("⚠️ No results found.")

# Upload CSV / SQL
st.markdown("---")
st.header("📤 Upload CSV or SQL File")
file = st.file_uploader("Upload CSV or SQL", type=["csv", "sql"])

if file:
    uploads = Path("uploads")
    uploads.mkdir(exist_ok=True)
    file_path = uploads / file.name
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    st.success(f"✅ Uploaded: {file.name}")

    if file.name.endswith(".csv"):
        try:
            df = pd.read_csv(file_path)
            st.dataframe(df)
            with sqlite3.connect("hr.db") as conn:
                df.to_sql("employees", conn, if_exists="replace", index=False)
            st.success("📥 Data saved to 'employees' table.")
        except Exception as e:
            st.error(f"❌ CSV Error: {e}")
    elif file.name.endswith(".sql"):
        try:
            with open(file_path) as f:
                sql_script = f.read()
            with sqlite3.connect("hr.db") as conn:
                conn.executescript(sql_script)
            st.success("📜 SQL script executed.")
        except Exception as e:
            st.error(f"❌ SQL Error: {e}")
