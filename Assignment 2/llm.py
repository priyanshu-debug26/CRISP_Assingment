import os
from dotenv import load_dotenv
from groq import Groq
import groq

from prompts import SYSTEM_PROMPT, PROMPT_TEMPLATES

# Load environment variables from the .env file
load_dotenv()

def get_mentor_response(task: str, code: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Sends the user's code and selected mentoring task to the Groq API.
    
    Args:
        task (str): The mentoring task (e.g., 'Explain Code', 'Find Bugs', etc.)
        code (str): The Java code string to analyze.
        model (str): The Groq model to use. Defaults to 'llama-3.3-70b-versatile'.
        
    Returns:
        str: The Markdown response from the LLM, or an error message if something fails.
    """
    # 1. Validate inputs
    if not code or not code.strip():
        return "Please enter some Java code to analyze."
        
    if task not in PROMPT_TEMPLATES:
        return f"Unknown task: '{task}'. Please choose a valid mentoring task."
        
    # 2. Get API key and initialize client dynamically
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_groq_api_key_here":
        return (
            "### ⚠️ API Key Configuration Missing\n\n"
            "The `GROQ_API_KEY` environment variable or key in the `.env` file is missing or not configured.\n\n"
            "**How to configure it:**\n"
            "1. Open the `.env` file in the root of the project: `AI-Java-Code-Mentor/.env`.\n"
            "2. Replace `your_groq_api_key_here` with your actual Groq API key (starts with `gsk_...`).\n"
            "3. Try again.\n\n"
            "*(If you do not have an API key, you can get one for free at [console.groq.com](https://console.groq.com/))* "
        )
        
    try:
        # Initialize the client with the provided API key
        client = Groq(api_key=api_key)
        
        # 3. Format prompt template with the input code
        user_prompt = PROMPT_TEMPLATES[task].format(code=code)
        
        # 4. Call the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model,
            temperature=0.2, # Lower temperature for analytical coding tasks
        )
        
        # 5. Extract and return the response content
        if chat_completion.choices and len(chat_completion.choices) > 0:
            return chat_completion.choices[0].message.content
        else:
            return "### Error\nNo response received from the model. Please try again."

    except groq.AuthenticationError:
        return (
            "### ❌ Authentication Error\n\n"
            "The provided Groq API key is invalid or unauthorized.\n\n"
            "**Steps to resolve:**\n"
            "- Double-check the key in your `.env` file (no quotes are needed around the key).\n"
            "- Make sure there are no accidental trailing spaces or characters.\n"
            "- Verify that your Groq account is active."
        )
    except groq.APIStatusError as e:
        return (
            f"### ❌ Groq API Error (Status {e.status_code})\n\n"
            f"The Groq service returned an error: `{e.message}`"
        )
    except groq.APIConnectionError:
        return (
            "### ❌ Connection Error\n\n"
            "Failed to connect to the Groq API servers. Please check your internet connection and try again."
        )
    except Exception as e:
        return f"### ❌ Unexpected Error\n\nAn unexpected error occurred: `{str(e)}`"
