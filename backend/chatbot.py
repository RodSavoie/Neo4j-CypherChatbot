import openai
import os

# Load OpenAI API Key from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")
openai.api_key = OPENAI_API_KEY

def chat(user_input):
    """Generates a Cypher query based on user input using OpenAI GPT-4o."""
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI that **ONLY** returns **valid Neo4j Cypher queries**. "
                    "Do NOT include explanations, apologies, or any text outside of the **raw Cypher query** itself. "
                    "The query **must** be correctly formatted and **ready to execute** in Neo4j."
                )
            },
            {"role": "user", "content": user_input}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o
            messages=messages,
            temperature=0
        )

        # Extract Cypher Query from API Response
        cypher_query = response.choices[0].message["content"].strip()

        # Debugging: Print OpenAI's Raw Response
        print("🛠 OpenAI Full Response:", response)
        print("✅ Generated Cypher Query:", cypher_query)

        # Ensure the query is valid (Basic Check)
        if not cypher_query.lower().startswith(("match", "call", "create", "return", "unwind", "merge")):
            raise ValueError("Generated response is not a valid Cypher query.")

        return cypher_query

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return "Error: Unable to generate a valid Cypher query."
