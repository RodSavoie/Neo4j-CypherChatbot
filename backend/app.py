from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import chat  # Ensure chatbot.py exists
from neo4j import GraphDatabase
import os

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:7689"  # Your Neo4j Bolt port
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")  # Replace with actual password

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Error: Empty query received. Please enter a valid question."})

    # Generate Cypher query using OpenAI-based chatbot
    cypher_query = chat(user_input)

    # Validate Cypher query before execution
    if "Error" in cypher_query or not cypher_query.strip().startswith(("MATCH", "CALL", "CREATE", "RETURN", "MERGE", "UNWIND")):
        return jsonify({"response": "Error: Unable to generate a valid Cypher query."})

    print(f"📝 Executing Cypher Query:\n{cypher_query}")

    # Execute the query in Neo4j
    try:
        with driver.session() as session:
            results = session.run(cypher_query).data()

        return jsonify({
            "generated_query": cypher_query,  # Return the Cypher query for debugging
            "response": results if results else "No results found."
        })

    except Exception as e:
        return jsonify({"response": f"Error executing query: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
