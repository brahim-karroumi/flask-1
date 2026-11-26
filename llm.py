from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY"),
    timeout=60,
    max_retries=0,
)

system_prompt = (
    "You are a helpful assistant that can answer questions and help with tasks."
    "You answered strictly in the same language as the user's input."
    "Keep the answers strict and small"
)

messages = [{"role": "system", "content": system_prompt}]


def chat_with_llm(user_input, context=None):

    messages.append({"role": "user", "content": user_input})
    if context:
        content = (
            "Answer the question using only the context below. "
            "If the context doesn't contain the answer, say so.\n\n"
            f"Context:\n{context}\n\nQuestion: {user_input}"
        )
    else:
        content = user_input
    
    messages.append({"role": "user", "content": content})
    response = client.chat.completions.create(
        model="openai/gpt-5-mini", messages=messages
    )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    return answer
