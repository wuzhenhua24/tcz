"""
Gemini REST API adapter for PageIndex
This module uses REST API instead of grpc to avoid SSL certificate issues
"""

import tiktoken
import logging
import os
from datetime import datetime
import time
import json
import PyPDF2
import copy
import asyncio
import pymupdf
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
import requests
import yaml
from pathlib import Path
from types import SimpleNamespace as config

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")  # Keep for compatibility

# Gemini REST API endpoint (use v1 instead of v1beta for better compatibility)
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1/models"

# Model mapping (use stable gemini-1.5-flash for better compatibility)
GEMINI_MODEL_MAP = {
    "gpt-4o": "gemini-1.5-flash",
    "gpt-4o-2024-11-20": "gemini-1.5-flash",
    "gpt-4o-mini": "gemini-1.5-flash",
    "gpt-4": "gemini-1.5-flash",
    "gpt-3.5-turbo": "gemini-1.5-flash",
}

def get_gemini_model_name(openai_model):
    """Convert OpenAI model name to Gemini model name"""
    return GEMINI_MODEL_MAP.get(openai_model, "gemini-1.5-flash")

def count_tokens(text, model=None):
    """
    Count tokens in text
    Note: For Gemini, we use tiktoken as approximation
    """
    if not text:
        return 0
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        return len(tokens)
    except Exception as e:
        # Fallback: rough estimation
        return len(text) // 4

def call_gemini_rest(model_name, prompt, api_key=None, temperature=0):
    """
    Call Gemini API using REST endpoint
    """
    if not api_key:
        api_key = GEMINI_API_KEY

    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    url = f"{GEMINI_API_BASE}/{model_name}:generateContent"

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": temperature,
            "topK": 1,
            "topP": 1,
        }
    }

    params = {
        "key": api_key
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        params=params,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

    result = response.json()

    # Extract text from response
    if "candidates" in result and len(result["candidates"]) > 0:
        candidate = result["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            parts = candidate["content"]["parts"]
            if len(parts) > 0 and "text" in parts[0]:
                text = parts[0]["text"]

                # Check finish reason
                finish_reason = "finished"
                if "finishReason" in candidate:
                    if candidate["finishReason"] == "MAX_TOKENS":
                        finish_reason = "max_output_reached"

                return text, finish_reason

    raise Exception(f"Unexpected response format: {result}")

def ChatGPT_API_with_finish_reason(model, prompt, api_key=None, chat_history=None):
    """
    Gemini REST adapter for ChatGPT API with finish reason
    """
    max_retries = 10
    gemini_model_name = get_gemini_model_name(model)

    # For now, we don't support chat history in REST mode
    # We just use the prompt directly
    full_prompt = prompt
    if chat_history:
        # Build conversation context
        context_parts = []
        for msg in chat_history:
            role = msg["role"]
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        context_parts.append(f"user: {prompt}")
        full_prompt = "\n".join(context_parts)

    for i in range(max_retries):
        try:
            text, finish_reason = call_gemini_rest(
                gemini_model_name,
                full_prompt,
                api_key=api_key or GEMINI_API_KEY,
                temperature=0
            )
            return text, finish_reason

        except Exception as e:
            print(f'************* Retrying (Gemini REST) ************* {e}')
            logging.error(f"Gemini REST Error: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                logging.error('Max retries reached for prompt: ' + prompt[:100])
                return "Error", "error"

def ChatGPT_API(model, prompt, api_key=None, chat_history=None):
    """
    Gemini REST adapter for ChatGPT API (main function)
    """
    text, _ = ChatGPT_API_with_finish_reason(model, prompt, api_key, chat_history)
    return text

async def ChatGPT_API_async(model, prompt, api_key=None):
    """
    Async version for Gemini REST API
    """
    max_retries = 10
    gemini_model_name = get_gemini_model_name(model)

    for i in range(max_retries):
        try:
            # Run REST call in executor
            loop = asyncio.get_event_loop()

            def _generate():
                text, _ = call_gemini_rest(
                    gemini_model_name,
                    prompt,
                    api_key=api_key or GEMINI_API_KEY,
                    temperature=0
                )
                return text

            result = await loop.run_in_executor(None, _generate)
            return result

        except Exception as e:
            print(f'************* Retrying Async (Gemini REST) ************* {e}')
            logging.error(f"Gemini REST Async Error: {e}")
            if i < max_retries - 1:
                await asyncio.sleep(2)
            else:
                logging.error('Max retries reached for async prompt')
                return "Error"

# Import other utility functions from original utils.py
try:
    from .utils import (
        extract_text_from_pdf,
        get_pdf_title,
        get_text_of_pages,
        sanitize_filename,
        get_pdf_name,
        list_to_tree,
        ConfigLoader,
    )
except ImportError:
    # If relative import fails, try absolute import
    import sys
    sys_path_backup = sys.path.copy()
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from utils import (
            extract_text_from_pdf,
            get_pdf_title,
            get_text_of_pages,
            sanitize_filename,
            get_pdf_name,
            list_to_tree,
            ConfigLoader,
        )
    finally:
        sys.path = sys_path_backup
