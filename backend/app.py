from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import os
from query_generator import generate_cypher_query
import json

app = Flask(__name__)
CORS(app)

# Load Neo4j credentials from environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7689")  # Adjust as needed
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def serialize_neo4j_data(record):
    """Converts Neo4j results into JSON-serializable format."""
    if isinstance(record, dict):  # Dictionary
        return {key: serialize_neo4j_data(value) for key, value in record.items()}
    if isinstance(record, list):  # List of records
        return [serialize_neo4j_data(item) for item in record]
    if hasattr(record, "items"):  # Dictionary-like structures
        return {k: serialize_neo4j_data(v) for k, v in record.items()}
    if hasattr(record, "get"):  # Handles Nodes & Relationships
        return {
            "id": record.id,
            "labels": list(record.labels) if hasattr(record, "labels") else [],
            "type": record.type if hasattr(record, "type") else None,
            "properties": dict(record)  # Convert properties to dictionary
        }
    if hasattr(record, "isoformat"):  # Handles date/time fields
        return record.isoformat()
    return record  # Return as-is for normal values


def run_cypher_query(cypher_query):
    """Executes a Cypher query and returns JSON-serializable results."""
    if not cypher_query or "Error" in cypher_query:
        return {"response": f"Error: Invalid Cypher query: {cypher_query}"}

    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            records = [serialize_neo4j_data(record) for record in result]
            return records
    except Exception as e:
        print(f"❌ Neo4j Query Execution Error: {e}")
        return {"response": f"Error executing query: {str(e)}"}


@app.route("/chat", methods=["POST"])
def chat_endpoint():
    """Handles user queries, generates Cypher, executes it, and returns results."""
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Error: Empty query received. Please enter a valid question."})

    # Generate Cypher query
    cypher_query = generate_cypher_query(user_input)

    if not cypher_query or not isinstance(cypher_query, str):
        return jsonify({"response": "Error: Unable to generate a valid Cypher query."})

    print(f"📝 Generated Cypher Query:\n{cypher_query}")

    # Execute the Cypher query
    query_result = run_cypher_query(cypher_query)

    return jsonify({
        "generated_query": cypher_query,
        "response": query_result
    })


if __name__ == "__main__":
    print("🚀 Starting Flask API for Neo4j-CypherChatbot...")
    app.run(host="0.0.0.0", port=5000, debug=True)
