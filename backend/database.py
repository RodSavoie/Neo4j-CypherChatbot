import os
from neo4j import GraphDatabase

# Load credentials from environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7689")  # Your Bolt port is 7689
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_cypher_query(query):
    """Run a Cypher query on Neo4j and return results."""
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result] or "No results found."
    except Exception as e:
        return f"Error executing query: {str(e)}"
