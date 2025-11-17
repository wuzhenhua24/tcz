"""
ZhipuAI (智谱AI) adapter for PageIndex
This module provides ZhipuAI GLM-4 compatible replacements for OpenAI API calls
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
import yaml
from pathlib import Path
from types import SimpleNamespace as config

# Import ZhipuAI SDK
from zhipuai import ZhipuAI

# Get API key from environment
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")  # Keep for compatibility

# Model mapping
ZHIPUAI_MODEL_MAP = {
    "gpt-4o": "glm-4-flash",
    "gpt-4o-2024-11-20": "glm-4-flash",
    "gpt-4o-mini": "glm-4-flash",
    "gpt-4": "glm-4-flash",
    "gpt-3.5-turbo": "glm-4-flash",
}

def get_zhipuai_model_name(openai_model):
    """Convert OpenAI model name to ZhipuAI model name"""
    return ZHIPUAI_MODEL_MAP.get(openai_model, "glm-4-flash")

def count_tokens(text, model=None):
    """
    Count tokens in text
    Note: For ZhipuAI, we use tiktoken as approximation
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

def ChatGPT_API_with_finish_reason(model, prompt, api_key=None, chat_history=None):
    """
    ZhipuAI adapter for ChatGPT API with finish reason
    """
    max_retries = 10
    zhipuai_model_name = get_zhipuai_model_name(model)

    if not api_key:
        api_key = ZHIPUAI_API_KEY

    if not api_key:
        raise ValueError("ZHIPUAI_API_KEY not set")

    for i in range(max_retries):
        try:
            # Initialize ZhipuAI client
            client = ZhipuAI(api_key=api_key)

            # Build messages
            messages = []
            if chat_history:
                messages = chat_history.copy()
            messages.append({"role": "user", "content": prompt})

            # Call ZhipuAI API
            response = client.chat.completions.create(
                model=zhipuai_model_name,
                messages=messages,
                temperature=0,
            )

            # Extract response
            text = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason

            # Map finish_reason to OpenAI format
            if finish_reason == "length":
                return text, "max_output_reached"
            else:
                return text, "finished"

        except Exception as e:
            print(f'************* Retrying (ZhipuAI) ************* {e}')
            logging.error(f"ZhipuAI Error: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                logging.error('Max retries reached for prompt: ' + prompt[:100])
                return "Error", "error"

def ChatGPT_API(model, prompt, api_key=None, chat_history=None):
    """
    ZhipuAI adapter for ChatGPT API (main function)
    """
    text, _ = ChatGPT_API_with_finish_reason(model, prompt, api_key, chat_history)
    return text

async def ChatGPT_API_async(model, prompt, api_key=None):
    """
    Async version for ZhipuAI API
    """
    max_retries = 10
    zhipuai_model_name = get_zhipuai_model_name(model)

    if not api_key:
        api_key = ZHIPUAI_API_KEY

    if not api_key:
        raise ValueError("ZHIPUAI_API_KEY not set")

    for i in range(max_retries):
        try:
            # Run in executor since ZhipuAI SDK doesn't have native async
            loop = asyncio.get_event_loop()

            def _generate():
                client = ZhipuAI(api_key=api_key)
                messages = [{"role": "user", "content": prompt}]
                response = client.chat.completions.create(
                    model=zhipuai_model_name,
                    messages=messages,
                    temperature=0,
                )
                return response.choices[0].message.content

            result = await loop.run_in_executor(None, _generate)
            return result

        except Exception as e:
            print(f'************* Retrying Async (ZhipuAI) ************* {e}')
            logging.error(f"ZhipuAI Async Error: {e}")
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
