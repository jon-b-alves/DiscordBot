import openai
import os
from config import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY

def chatgpt_response(prompt):
    response = openai.Completion.create(
        model = "text-davinci-003",
        promt = prompt,
        temperature = 1,
        max_tokens = 100
    )
    response_dict = response.get("choices")
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]["text"]
        return prompt_response 
