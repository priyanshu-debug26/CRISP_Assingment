import json
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from prompts import resume_analyzer_prompt

def analyze_resume(resume_text: str, provider: str, api_key: str, model_name: str, temperature: float) -> dict:
    """
    Invokes the LLM to analyze the provided resume text based on a recruiter prompt
    and parses the result into a Python dictionary.
    
    Parameters:
        resume_text (str): The raw text extracted from the resume PDF.
        provider (str): 'groq' or 'openai'.
        api_key (str): The user's API Key.
        model_name (str): The specific LLM model to run.
        temperature (float): Controls response creativity.
        
    Returns:
        dict: Parsed analysis containing score, strengths, weaknesses, skills, ATS compatibility, etc.
        
    Raises:
        ValueError: If inputs are invalid or output parsing fails.
        RuntimeError: If LLM API call fails or network issues occur.
    """
    # 1. Input Validation
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text content is empty. Cannot perform evaluation.")
    
    # 2. LLM Client Construction
    provider_clean = provider.strip().lower()
    try:
        if provider_clean == "groq":
            llm = ChatGroq(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature
            )
        elif provider_clean == "openai":
            llm = ChatOpenAI(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature
            )
        else:
            raise ValueError(f"LLM Provider '{provider}' is not supported. Use 'groq' or 'openai'.")
    except Exception as init_err:
        raise RuntimeError(f"Could not connect to {provider.capitalize()} client: {str(init_err)}")

    # 3. Chain Invocation
    try:
        chain = resume_analyzer_prompt | llm | StrOutputParser()
        raw_response = chain.invoke({"resume_text": resume_text})
    except Exception as api_err:
        raise RuntimeError(f"LLM API request failed: {str(api_err)}")

    # 4. JSON Cleaning and Parsing
    response_text = raw_response.strip()
    
    # Remove markdown codeblock tags if the model wraps the JSON
    if response_text.startswith("```"):
        response_text = re.sub(r"^```(?:json)?\n", "", response_text)
        response_text = re.sub(r"\n```$", "", response_text)
    response_text = response_text.strip()

    try:
        parsed_data = json.loads(response_text)
        
        # Validate that required keys are present
        required_keys = ["score", "strengths", "weaknesses", "tech_skills", "soft_skills", "ats_feedback", "missing_keywords", "job_roles", "improvements"]
        for key in required_keys:
            if key not in parsed_data:
                # Add default empty list or default value if missing to keep application running
                if key == "score":
                    parsed_data[key] = 50
                else:
                    parsed_data[key] = ["No details provided by model."]
                    
        return parsed_data
        
    except json.JSONDecodeError as jde:
        raise ValueError(
            f"The LLM returned a response that could not be parsed as valid JSON. "
            f"Please verify your model configuration or try again.\n\nError: {str(jde)}"
        )
