from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv("keys.env") 

def request_message_to_ai(message):
    try:
        client = OpenAI(
            api_key=os.getenv("api_key")
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"xatolik {e}"
        
