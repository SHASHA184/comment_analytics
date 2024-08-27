import google.generativeai as genai
import os
import asyncio

GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")

genai.configure(api_key=GOOGLE_AI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-alpha")


async def generate_text(prompt: str) -> str:
    return await model.generate_content_async(prompt)


async def moderate_text(text: str) -> str:
    prompt = f"Moderate the following text: {text}. Check it on the following criteria: hate speech, offensive language, and personal attacks. If the text violates any of these criteria, please answer with 'yes'. Otherwise, answer with 'no'."
    return await generate_text(prompt)


if __name__ == "__main__":
    print(asyncio.run(moderate_text("I hate you!")))
    print(asyncio.run(moderate_text("You are so stupid!")))
    print(asyncio.run(moderate_text("How are you today?")))
    print(asyncio.run(moderate_text("I will kill you!")))
