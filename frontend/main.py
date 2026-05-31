from groq import Groq
from langchain_groq import ChatGroq
from pydantic import SecretStr
import os
import traceback
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = (
    "You are TanuShree, a warm and helpful AI assistant for Tanman Restro — "
    "a cozy, food-loving restaurant.\n"
    "Answer questions about menu, hours, reservations, and "
    "recommendations.\n"
    "Be enthusiastic about food, use food emojis occasionally 🍕🍜🍣, "
    "and keep responses concise but warm."
)


groq_api_key = os.environ.get("GROQ_API_KEY")
secret_api_key = SecretStr(groq_api_key) if groq_api_key is not None else None

llm = ChatGroq(
    api_key=secret_api_key,
    model="llama-3.1-8b-instant"
)


def get_answer(user_question: str, model_name: str = "llama-3.1-8b-instant") -> str:
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "❌ Groq Api."
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question},
            ],
            temperature=0.7,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return (
            f"❌ Error: {type(e).__name__}: {str(e)}\n\n"
            f"{traceback.format_exc()}"
        )


if __name__ == "__main__":
    test_q = "What are your most popular dishes?"
    print("Q:", test_q)
    print("A:", get_answer(test_q))