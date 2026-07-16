from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
api_key=API_KEY, 
base_url=BASE_URL
)

def chat(message: list) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=message,
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    messages = [
        {"role": "user", 
         "content": "Tell exact current time and date."
         }
    ]

    response = chat(messages)
    print(response)