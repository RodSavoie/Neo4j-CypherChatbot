import openai
import os

# Load OpenAI API Key from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")
openai.api_key = OPENAI_API_KEY

def generate_cypher_query(user_input):
    """Generates a Cypher query based on user input using OpenAI GPT-4o."""
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI that exclusively generates **valid Neo4j Cypher queries**. "
                    "Do NOT include explanations, apologies, or any non-Cypher text. "
                    "Only return the **raw Cypher query** without code blocks or formatting."
                )
            },
            {"role": "user", "content": user_input}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",  # Ensure GPT-4o is used
            messages=messages,
            temperature=0
        )

        # Extract Cypher Query from API Response
        cypher_query = response.choices[0].message.content.strip()

        if not cypher_query.startswith("MATCH") and not cypher_query.startswith("RETURN"):
            print(f"❌ Invalid Cypher Query Generated: {cypher_query}")
            return "Error: OpenAI did not return a valid Cypher query."

        print(f"✅ Generated Cypher Query: {cypher_query}")
        return cypher_query

    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        return "Error: Unable to generate a valid Cypher query."
