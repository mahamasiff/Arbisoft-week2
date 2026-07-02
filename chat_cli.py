import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = "cohere/north-mini-code:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def chat(model: str) -> None:
    messages = []
    print(f"Chatting with {model}. Type 'exit' or 'quit' to stop, 'reset' to clear history.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            messages.clear()
            print("Conversation history cleared.\n")
            continue

        messages.append({"role": "user", "content": user_input})

        print(f"{model}: ", end="", flush=True)
        reply = ""
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
                reply += delta
        except Exception as e:
            print(f"\n[error] {e}")
            messages.pop()
            continue

        print("\n")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not set in environment or .env file.")
        sys.exit(1)
    chat(model)
