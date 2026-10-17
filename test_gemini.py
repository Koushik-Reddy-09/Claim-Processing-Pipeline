
from app.gemini_client import ask_gemini

try:
    answer = ask_gemini(
        "Reply with exactly: Gemini connection successful"
    )
    print(answer)
except Exception as error:
    print("Gemini connection failed.")
    print("Error:", error)
