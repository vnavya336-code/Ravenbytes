import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

print("GEMINI MODEL LOADED:", MODEL)


def ask_ai(question):

    if not API_KEY or API_KEY == "your_api_key":
        return "Gemini API key is missing. Please check your .env file."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODEL}:generateContent"
    )

    prompt = f"""
You are ScholarBridge AI Assistant.

Help students in Karnataka, India.

You help:
1. Students who passed 10th standard.
2. Students who passed 12th standard.
3. Undergraduate engineering students.

Answer questions about:
- Scholarships
- Karnataka government schemes
- Eligibility requirements
- Required documents
- Application procedures
- Application deadlines

Rules:
- Use simple English.
- Give beginner-friendly answers.
- Never invent scholarship names or deadlines.
- Never claim official eligibility confirmation.
- Recommend checking official websites.
- If you don't know, say so.

Student question: {question}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Retry temporary server errors
    for attempt in range(3):

        try:

            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": API_KEY
                },
                json=payload,
                timeout=60
            )

            if response.status_code in [429, 500, 502, 503, 504]:

                print("GEMINI TEMPORARY ERROR:", response.status_code)
                print(response.text)

                if attempt < 2:
                    wait_time = 2 ** (attempt + 1)
                    print("Retrying in", wait_time, "seconds...")
                    time.sleep(wait_time)
                    continue

                return (
                    "Gemini is temporarily busy. "
                    "Please wait a few seconds and try again."
                )

            response.raise_for_status()

            data = response.json()

            candidates = data.get("candidates", [])

            if not candidates:
                print("GEMINI RESPONSE:", data)
                return "Sorry! Gemini did not generate an answer. Please try again."

            parts = candidates[0].get("content", {}).get("parts", [])

            answer = "\n".join(
                part["text"]
                for part in parts
                if "text" in part
            )

            if answer:
                return answer

            return "Sorry! No answer was generated. Please try again."

        except requests.exceptions.Timeout:

            print("GEMINI TIMEOUT")

            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            return "Gemini took too long to respond. Please try again."

        except requests.exceptions.RequestException as e:

            print("GEMINI API ERROR:", str(e))

            if e.response is not None:
                print("STATUS CODE:", e.response.status_code)
                print("ERROR DETAILS:", e.response.text)

            return "Unable to connect to Gemini. Please try again."

        except (KeyError, IndexError, TypeError) as e:

            print("GEMINI RESPONSE ERROR:", str(e))

            return "Sorry! I couldn't generate an answer."

    return "Please try again later."