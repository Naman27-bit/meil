import sys
import io
import os
import traceback

# Fix Unicode/emoji encoding on Windows & Streamlit Cloud
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

os.environ["PYTHONIOENCODING"] = "utf-8"

from groq import Groq
from langchain_groq import ChatGroq
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = (
    "You are TanuShree, a warm and helpful AI assistant for Tanman Restro — "
    "a cozy, food-loving restaurant.\n"
    "Answer questions about menu, hours, reservations, and "
    "recommendations.\n"
    "Be enthusiastic about food, use food emojis occasionally, "
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
            return "Wrong Groq API key. Please set it in the sidebar."
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
        answer = response.choices[0].message.content.strip()
        # Ensure safe encoding before returning
        return answer.encode('utf-8', errors='replace').decode('utf-8')
    except Exception as e:
        return (
            f"Error: {type(e).__name__}: {str(e)}\n\n"
            f"{traceback.format_exc()}"
        )


if __name__ == "__main__":
    test_q = "What are your most popular dishes?"
    print("Q:", test_q)
    answer = get_answer(test_q)
    print("A:", answer.encode('utf-8', errors='replace').decode('utf-8'))
