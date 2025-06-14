import streamlit as st
import sqlite3
import os
import pandas as pd
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load GROQ API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Page setup
st.set_page_config(page_title="📊 Ask Your HR Database", page_icon="📊")
st.title("📊 Ask Your HR Database")
st.caption("Ask questions in plain English (e.g., 'Show average salary by department')")

# Global DB name
DB_NAME = "hr.db"

# 🔄 Get table schema dynamically
def get_table_schema():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(employees);")
            schema_info = cursor.fetchall()
            return [col[1] for col in schema_info]
    except Exception:
        return []

# 🔍 Generate SQL from question
def generate_sql(question, columns):
    schema_str = f"Table: employees({', '.join(columns)})"
    prompt = f"""
You are a helpful assistant. Convert the natural language question into a valid SQLite query.

Question: {question}
{schema_str}
Only return the SQL query.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 🛠 Execute SQL
def execute_sql_query(query):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        return rows, columns
    except Exception as e:
        return str(e), []

# 💬 Input box
question = st.text_input("Ask a question:")

# 🧠 Process question
if question:
    with st.spinner("🧠 Thinking..."):
        columns = get_table_schema()
        if not columns:
            st.warning("⚠️ No data available yet. Please upload a CSV first.")
        else:
            sql = generate_sql(question, columns)
            st.subheader("💡 Generated SQL")
            st.code(sql, language="sql")

            result, cols = execute_sql_query(sql)

            if isinstance(result, str):
                st.error(f"❌ SQL Error: {result}")
            elif result:
                st.success("✅ Result:")
                st.dataframe([dict(zip(cols, row)) for row in result])
            else:
                st.warning("ℹ️ No results found.")

# 📤 File Upload Section
st.markdown("---")
st.header("📤 Upload a File (CSV or SQL)")
uploaded_file = st.file_uploader("Choose a CSV or SQL file", type=['csv', 'sql'])

if uploaded_file:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    file_path = uploads_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File uploaded: `{uploaded_file.name}`")

    if uploaded_file.name.endswith(".csv"):
        try:
            df = pd.read_csv(file_path)
            st.write("📄 Preview of uploaded CSV:")
            st.dataframe(df)

            with sqlite3.connect(DB_NAME) as conn:
                df.to_sql("employees", conn, if_exists="replace", index=False)

            st.success("📥 CSV data inserted into 'employees' table.")
        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")

    elif uploaded_file.name.endswith(".sql"):
        try:
            with open(file_path, "r") as sql_file:
                sql_script = sql_file.read()
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_script)
            st.success("📜 SQL script executed successfully.")
        except Exception as e:
            st.error(f"❌ Error executing SQL script: {e}")
