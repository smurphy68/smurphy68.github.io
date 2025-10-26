from openai import OpenAI
from open_ai_secrets import OPENAI_API_KEY

def gpt_chat_response(gpt_prompt):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=gpt_prompt,
        max_tokens = 100
    ).choices[-1].text
    print(response)
    return response
