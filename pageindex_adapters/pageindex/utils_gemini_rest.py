"""
Gemini REST API adapter for PageIndex
This module uses REST API instead of grpc to avoid SSL certificate issues
"""

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

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

# Model mapping (use gemini-2.5-flash - latest stable model)
GEMINI_MODEL_MAP = {
    "gpt-4o": "gemini-2.5-flash",
    "gpt-4o-2024-11-20": "gemini-2.5-flash",
    "gpt-4o-mini": "gemini-2.5-flash",
    "gpt-4": "gemini-2.5-flash",
    "gpt-3.5-turbo": "gemini-2.5-flash",
}

def get_gemini_model_name(openai_model):
    """Convert OpenAI model name to Gemini model name"""
    return GEMINI_MODEL_MAP.get(openai_model, "gemini-2.5-flash")

def count_tokens(text, model=None):
    """
    Count tokens in text
    Note: For Gemini, we use tiktoken as approximation
    """
    if not text:
        return 0
    if HAS_TIKTOKEN:
        try:
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = enc.encode(text)
            return len(tokens)
        except Exception as e:
            # Fallback: rough estimation
            return len(text) // 4
    else:
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

# ============================================================================
# Utility functions from original PageIndex utils.py
# Copied here to avoid circular import issues with sys.modules injection
# ============================================================================

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def get_pdf_title(pdf_path):
    """Get PDF title from metadata"""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    meta = pdf_reader.metadata
    title = meta.title if meta and meta.title else 'Untitled'
    return title

def get_text_of_pages(pdf_path, start_page, end_page, tag=True):
    """Extract text from specific page range"""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(start_page-1, end_page):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        if tag:
            text += f"<start_index_{page_num+1}>\n{page_text}\n<end_index_{page_num+1}>\n"
        else:
            text += page_text
    return text

def sanitize_filename(filename, replacement='-'):
    """Sanitize filename by replacing invalid characters"""
    return filename.replace('/', replacement)

def get_pdf_name(pdf_path):
    """Get PDF filename or title"""
    if isinstance(pdf_path, str):
        pdf_name = os.path.basename(pdf_path)
    elif isinstance(pdf_path, BytesIO):
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        meta = pdf_reader.metadata
        pdf_name = meta.title if meta and meta.title else 'Untitled'
        pdf_name = sanitize_filename(pdf_name)
    return pdf_name

def list_to_tree(data):
    """Convert flat list structure to tree structure"""
    def get_parent_structure(structure):
        if not structure:
            return None
        parts = str(structure).split('.')
        return '.'.join(parts[:-1]) if len(parts) > 1 else None

    nodes = {}
    root_nodes = []

    for item in data:
        structure = item.get('structure')
        node = {
            'title': item.get('title'),
            'start_index': item.get('start_index'),
            'end_index': item.get('end_index'),
            'nodes': []
        }

        nodes[structure] = node
        parent_structure = get_parent_structure(structure)

        if parent_structure:
            if parent_structure in nodes:
                nodes[parent_structure]['nodes'].append(node)
            else:
                root_nodes.append(node)
        else:
            root_nodes.append(node)

    def clean_node(node):
        if not node['nodes']:
            del node['nodes']
        else:
            for child in node['nodes']:
                clean_node(child)
        return node

    return [clean_node(node) for node in root_nodes]

def get_json_content(response):
    """Extract JSON content from markdown code blocks"""
    start_idx = response.find("```json")
    if start_idx != -1:
        start_idx += 7
        response = response[start_idx:]

    end_idx = response.rfind("```")
    if end_idx != -1:
        response = response[:end_idx]

    json_content = response.strip()
    return json_content

def extract_json(content):
    """Parse JSON from text, handling common formatting issues"""
    try:
        start_idx = content.find("```json")
        if start_idx != -1:
            start_idx += 7
            end_idx = content.rfind("```")
            json_content = content[start_idx:end_idx].strip()
        else:
            json_content = content.strip()

        json_content = json_content.replace('None', 'null')
        json_content = json_content.replace('\n', ' ').replace('\r', ' ')
        json_content = ' '.join(json_content.split())

        return json.loads(json_content)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to extract JSON: {e}")
        try:
            json_content = json_content.replace(',]', ']').replace(',}', '}')
            return json.loads(json_content)
        except:
            logging.error("Failed to parse JSON even after cleanup")
            return {}
    except Exception as e:
        logging.error(f"Unexpected error while extracting JSON: {e}")
        return {}

def write_node_id(data, node_id=0):
    """Recursively assign node IDs to tree structure"""
    if isinstance(data, dict):
        data['node_id'] = str(node_id).zfill(4)
        node_id += 1
        for key in list(data.keys()):
            if 'nodes' in key:
                node_id = write_node_id(data[key], node_id)
    elif isinstance(data, list):
        for index in range(len(data)):
            node_id = write_node_id(data[index], node_id)
    return node_id

def convert_physical_index_to_int(data):
    """Convert physical_index strings to integers"""
    if isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict) and 'physical_index' in data[i]:
                if isinstance(data[i]['physical_index'], str):
                    if data[i]['physical_index'].startswith('<physical_index_'):
                        data[i]['physical_index'] = int(data[i]['physical_index'].split('_')[-1].rstrip('>').strip())
                    elif data[i]['physical_index'].startswith('physical_index_'):
                        data[i]['physical_index'] = int(data[i]['physical_index'].split('_')[-1].strip())
    elif isinstance(data, str):
        if data.startswith('<physical_index_'):
            data = int(data.split('_')[-1].rstrip('>').strip())
        elif data.startswith('physical_index_'):
            data = int(data.split('_')[-1].strip())
        if isinstance(data, int):
            return data
        else:
            return None
    return data

def convert_page_to_int(data):
    """Convert page strings to integers"""
    for item in data:
        if 'page' in item and isinstance(item['page'], str):
            try:
                item['page'] = int(item['page'])
            except ValueError:
                pass
    return data

def get_page_tokens(pdf_path, model="gpt-4o-2024-11-20", pdf_parser="PyPDF2"):
    """Extract text and count tokens for each PDF page"""
    if pdf_parser == "PyPDF2":
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        page_list = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            token_length = count_tokens(page_text, model)
            page_list.append((page_text, token_length))
        return page_list
    elif pdf_parser == "PyMuPDF":
        if isinstance(pdf_path, BytesIO):
            pdf_stream = pdf_path
            doc = pymupdf.open(stream=pdf_stream, filetype="pdf")
        elif isinstance(pdf_path, str) and os.path.isfile(pdf_path) and pdf_path.lower().endswith(".pdf"):
            doc = pymupdf.open(pdf_path)
        page_list = []
        for page in doc:
            page_text = page.get_text()
            token_length = count_tokens(page_text, model)
            page_list.append((page_text, token_length))
        return page_list
    else:
        raise ValueError(f"Unsupported PDF parser: {pdf_parser}")

class JsonLogger:
    """Logger that writes to JSON files"""
    def __init__(self, file_path):
        pdf_name = file_path if isinstance(file_path, str) else 'Untitled'
        if isinstance(file_path, str):
            pdf_name = os.path.basename(file_path)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{pdf_name}_{current_time}.json"
        os.makedirs("./logs", exist_ok=True)
        self.log_data = []

    def log(self, level, message, **kwargs):
        if isinstance(message, dict):
            self.log_data.append(message)
        else:
            self.log_data.append({'message': message})

        with open(self._filepath(), "w") as f:
            json.dump(self.log_data, f, indent=2)

    def info(self, message, **kwargs):
        self.log("INFO", message, **kwargs)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)

    def debug(self, message, **kwargs):
        self.log("DEBUG", message, **kwargs)

    def exception(self, message, **kwargs):
        kwargs["exception"] = True
        self.log("ERROR", message, **kwargs)

    def _filepath(self):
        return os.path.join("logs", self.filename)

def structure_to_list(structure):
    """Convert tree structure to flat list of nodes"""
    if isinstance(structure, dict):
        nodes = []
        nodes.append(structure)
        if 'nodes' in structure:
            nodes.extend(structure_to_list(structure['nodes']))
        return nodes
    elif isinstance(structure, list):
        nodes = []
        for item in structure:
            nodes.extend(structure_to_list(item))
        return nodes

def get_nodes(structure):
    """Get all nodes from structure"""
    if isinstance(structure, dict):
        structure_node = copy.deepcopy(structure)
        structure_node.pop('nodes', None)
        nodes = [structure_node]
        for key in list(structure.keys()):
            if 'nodes' in key:
                nodes.extend(get_nodes(structure[key]))
        return nodes
    elif isinstance(structure, list):
        nodes = []
        for item in structure:
            nodes.extend(get_nodes(item))
        return nodes

def get_leaf_nodes(structure):
    """Get only leaf nodes from structure"""
    if isinstance(structure, dict):
        if not structure.get('nodes'):
            structure_node = copy.deepcopy(structure)
            structure_node.pop('nodes', None)
            return [structure_node]
        else:
            leaf_nodes = []
            for key in list(structure.keys()):
                if 'nodes' in key:
                    leaf_nodes.extend(get_leaf_nodes(structure[key]))
            return leaf_nodes
    elif isinstance(structure, list):
        leaf_nodes = []
        for item in structure:
            leaf_nodes.extend(get_leaf_nodes(item))
        return leaf_nodes

def is_leaf_node(data, node_id):
    """Check if a node is a leaf node"""
    def find_node(data, node_id):
        if isinstance(data, dict):
            if data.get('node_id') == node_id:
                return data
            for key in data.keys():
                if 'nodes' in key:
                    result = find_node(data[key], node_id)
                    if result:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = find_node(item, node_id)
                if result:
                    return result
        return None

    node = find_node(data, node_id)

    if node and not node.get('nodes'):
        return True
    return False

def get_last_node(structure):
    """Get the last node from structure"""
    return structure[-1]

def get_text_of_pdf_pages(pdf_pages, start_page, end_page):
    """Extract text from PDF page range"""
    text = ""
    for page_num in range(start_page-1, end_page):
        text += pdf_pages[page_num][0]
    return text

def get_text_of_pdf_pages_with_labels(pdf_pages, start_page, end_page):
    """Extract text from PDF pages with page labels"""
    text = ""
    for page_num in range(start_page-1, end_page):
        text += f"<physical_index_{page_num+1}>\n{pdf_pages[page_num][0]}\n<physical_index_{page_num+1}>\n"
    return text

def get_number_of_pages(pdf_path):
    """Get total number of pages in PDF"""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    num = len(pdf_reader.pages)
    return num

def add_node_text(node, pdf_pages):
    """Add text content to nodes from PDF pages"""
    if isinstance(node, dict):
        start_page = node.get('start_index')
        end_page = node.get('end_index')
        node['text'] = get_text_of_pdf_pages(pdf_pages, start_page, end_page)
        if 'nodes' in node:
            add_node_text(node['nodes'], pdf_pages)
    elif isinstance(node, list):
        for index in range(len(node)):
            add_node_text(node[index], pdf_pages)
    return

async def generate_node_summary(node, model=None):
    """Generate summary for a single node"""
    prompt = f"""You are given a part of a document, your task is to generate a description of the partial document about what are main points covered in the partial document.

    Partial Document Text: {node['text']}

    Directly return the description, do not include any other text.
    """
    response = await ChatGPT_API_async(model, prompt)
    return response

async def generate_summaries_for_structure(structure, model=None):
    """Generate summaries for all nodes in structure"""
    nodes = structure_to_list(structure)
    tasks = [generate_node_summary(node, model=model) for node in nodes]
    summaries = await asyncio.gather(*tasks)

    for node, summary in zip(nodes, summaries):
        node['summary'] = summary
    return structure

def remove_structure_text(data):
    """Remove text field from all nodes"""
    if isinstance(data, dict):
        data.pop('text', None)
        if 'nodes' in data:
            remove_structure_text(data['nodes'])
    elif isinstance(data, list):
        for item in data:
            remove_structure_text(item)
    return data

def create_clean_structure_for_description(structure):
    """Create clean structure with only title, node_id, summary, prefix_summary"""
    if isinstance(structure, dict):
        clean_node = {}
        for key in ['title', 'node_id', 'summary', 'prefix_summary']:
            if key in structure:
                clean_node[key] = structure[key]

        if 'nodes' in structure and structure['nodes']:
            clean_node['nodes'] = create_clean_structure_for_description(structure['nodes'])

        return clean_node
    elif isinstance(structure, list):
        return [create_clean_structure_for_description(item) for item in structure]
    else:
        return structure

def generate_doc_description(structure, model=None):
    """Generate document description"""
    prompt = f"""Your are an expert in generating descriptions for a document.
    You are given a structure of a document. Your task is to generate a one-sentence description for the document, which makes it easy to distinguish the document from other documents.

    Document Structure: {structure}

    Directly return the description, do not include any other text.
    """
    response = ChatGPT_API(model, prompt)
    return response

def post_processing(structure, end_physical_index):
    """Post process structure to add start/end indices"""
    for i, item in enumerate(structure):
        item['start_index'] = item.get('physical_index')
        if i < len(structure) - 1:
            if structure[i + 1].get('appear_start') == 'yes':
                item['end_index'] = structure[i + 1]['physical_index']-1
            else:
                item['end_index'] = structure[i + 1]['physical_index']
        else:
            item['end_index'] = end_physical_index
    tree = list_to_tree(structure)
    if len(tree)!=0:
        return tree
    else:
        for node in structure:
            node.pop('appear_start', None)
            node.pop('physical_index', None)
        return structure

def add_preface_if_needed(data):
    """Add preface node if document doesn't start at page 1"""
    if not isinstance(data, list) or not data:
        return data

    if data[0]['physical_index'] is not None and data[0]['physical_index'] > 1:
        preface_node = {
            "structure": "0",
            "title": "Preface",
            "physical_index": 1,
        }
        data.insert(0, preface_node)
    return data

class JsonLogger:
    """Logger that writes to JSON files"""
    def __init__(self, file_path):
        pdf_name = file_path if isinstance(file_path, str) else 'Untitled'
        if isinstance(file_path, str):
            pdf_name = os.path.basename(file_path)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{pdf_name}_{current_time}.json"
        os.makedirs("./logs", exist_ok=True)
        self.log_data = []

    def log(self, level, message, **kwargs):
        if isinstance(message, dict):
            self.log_data.append(message)
        else:
            self.log_data.append({'message': message})

        with open(self._filepath(), "w") as f:
            json.dump(self.log_data, f, indent=2)

    def info(self, message, **kwargs):
        self.log("INFO", message, **kwargs)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)

    def debug(self, message, **kwargs):
        self.log("DEBUG", message, **kwargs)

    def exception(self, message, **kwargs):
        kwargs["exception"] = True
        self.log("ERROR", message, **kwargs)

    def _filepath(self):
        return os.path.join("logs", self.filename)

class ConfigLoader:
    """Configuration loader for PageIndex"""
    def __init__(self, default_path: str = None):
        if default_path is None:
            # Try to find config.yaml in pageindex package
            try:
                import pageindex
                default_path = Path(pageindex.__file__).parent / "config.yaml"
            except:
                default_path = Path(__file__).parent / "config.yaml"
        self._default_dict = self._load_yaml(default_path) if os.path.exists(default_path) else {}

    @staticmethod
    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _validate_keys(self, user_dict):
        unknown_keys = set(user_dict) - set(self._default_dict)
        if unknown_keys:
            raise ValueError(f"Unknown config keys: {unknown_keys}")

    def load(self, user_opt=None) -> config:
        if user_opt is None:
            user_dict = {}
        elif isinstance(user_opt, config):
            user_dict = vars(user_opt)
        elif isinstance(user_opt, dict):
            user_dict = user_opt
        else:
            raise TypeError("user_opt must be dict, config or None")

        self._validate_keys(user_dict)
        merged = {**self._default_dict, **user_dict}
        return config(**merged)
