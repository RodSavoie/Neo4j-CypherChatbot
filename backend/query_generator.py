import os
import re
from openai import OpenAI

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set it in environment variables.")

client = OpenAI()  # Automatically loads API key

def extract_cypher_query(response_text):
    """Extracts only the Cypher query from OpenAI's response."""
    # Remove potential Markdown formatting
    response_text = response_text.replace("```cypher", "").replace("```", "").strip()

    # Ensure the response starts with a Cypher keyword
    valid_cypher_keywords = ["MATCH", "CREATE", "MERGE", "RETURN", "WITH", "CALL"]
    for keyword in valid_cypher_keywords:
        if response_text.startswith(keyword):
            return response_text

    return "Error: OpenAI did not return a valid Cypher query."

def generate_cypher_query(user_input, limit=10):
    """Generate a valid Cypher query for Neo4j 5.26.1 using GPT-4o."""
    if not user_input.strip():
        return "Error: Empty user input."

    prompt = f"""
    You are an AI that generates Cypher queries for a Neo4j database.

    ⚙️ Environment:
    - Neo4j 5.26.1 with APOC Core + Extended 5.26.1
    - NeoDash 2.4.9
    - Bolt connection on `bolt://localhost:7689`
    - Running on Windows 11 with Neo4j Desktop 1.6.1
    - Labels available: Transaction, Account, _Neodash_Dashboard, Metrics

    🔹 Rules:
    1. Only generate valid Cypher queries that work in Neo4j 5.26.1.
    2. Do NOT use `dbms.procedures()`, as it is restricted in this environment.
    3. Use only these labels: Transaction, Account, _Neodash_Dashboard, Metrics.
    4. Do NOT use labels that do not exist in the database.
    5. Default to `LIMIT 10` for general queries unless specified.
    6. Do NOT use `LIMIT` when counting (`RETURN count(*)`).
    7. Always output the Cypher query **ONLY** without explanations.

    Example Queries:
    - "Find all accounts" -> "MATCH (a:Account) RETURN a LIMIT 10"
    - "Show all transactions" -> "MATCH (t:Transaction) RETURN t LIMIT 10"
    - "Get metrics data" -> "MATCH (m:Metrics) RETURN m LIMIT 10"
    - "Find all dashboards" -> "MATCH (d:_Neodash_Dashboard) RETURN d LIMIT 10"
    - "How many transactions over $10,000?" -> "MATCH (t:Transaction) WHERE t.trAmount > 10000 RETURN count(t) AS transactionCount"

    Now, generate a Cypher query for:
    {user_input}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o for better performance
            messages=[
                {"role": "system", "content": "You are a Neo4j Cypher expert. Only return valid Cypher queries."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100
        )

        cypher_query = response.choices[0].message.content.strip()
        cleaned_query = extract_cypher_query(cypher_query)

        return cleaned_query

    except Exception as e:
        return f"Error calling OpenAI: {str(e)}"
