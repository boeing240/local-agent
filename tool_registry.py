import math

from tools.web_search import web_search
from tools.file_ops import read_file, write_file, search_files
from tools.tasks import add_task, list_tasks, complete_task, add_note, list_notes
from tools.shell import run_command
from tools.text_tools import translate_text, summarize_text, generate_code
from tools.clipboard import clipboard_read, clipboard_write
from tools.data_tools import read_csv, read_json, analyze_csv
from tools.pdf_reader import read_pdf


def calculate(expression: str) -> str:
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        allowed["abs"] = abs
        allowed["round"] = round
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


def edit_text(text: str, instruction: str) -> str:
    return f"INSTRUCTION: {instruction}\n\nTEXT TO EDIT:\n{text}"


def write_email(to: str, subject: str, context: str) -> str:
    return f"Write a professional email.\nTo: {to}\nSubject: {subject}\nContext: {context}"


def check_spelling(text: str) -> str:
    return f"Check the following text for spelling and grammar errors. List each error and suggest a correction:\n\n{text}"

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using DuckDuckGo. Use this to answer questions about current events or anything requiring up-to-date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                    "max_results": {"type": "integer", "description": "Number of results to return (default 5)"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full contents of a file from the filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative path to the file"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file, creating it if it does not exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for a text pattern inside all files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory to search in"},
                    "pattern": {"type": "string", "description": "Text pattern to search for"},
                },
                "required": ["directory", "pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the task list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The task description"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks and their completion status.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as done by its ID number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The numeric ID of the task"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_note",
            "description": "Save a note for later reference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The note content"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all saved notes.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_text",
            "description": "Edit, improve or rewrite a text according to an instruction. Use for proofreading, paraphrasing, making text more formal/casual, shortening, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The original text to edit"},
                    "instruction": {"type": "string", "description": "What to do with the text, e.g. 'make it more formal', 'fix grammar', 'shorten it'"},
                },
                "required": ["text", "instruction"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_email",
            "description": "Compose a professional email. Use when the user asks to write or draft an email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient name or role, e.g. 'manager', 'client John'"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "context": {"type": "string", "description": "What the email should be about"},
                },
                "required": ["to", "subject", "context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_spelling",
            "description": "Check text for spelling and grammar errors and suggest corrections.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to check"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Translate text to another language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "target_language": {"type": "string", "description": "Target language, e.g. 'Russian', 'English', 'German'"},
                },
                "required": ["text", "target_language"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_text",
            "description": "Summarize a long text or document into a short summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to summarize"},
                    "max_sentences": {"type": "integer", "description": "Maximum number of sentences in the summary (default 3)"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_code",
            "description": "Generate code based on a description. Use when the user asks to write a script, function, or program.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "What the code should do"},
                    "language": {"type": "string", "description": "Programming language (default Python)"},
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Supports standard math operations and functions like sqrt, sin, cos, log, pow, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate, e.g. '2 + 2', 'sqrt(144)', 'sin(3.14)'"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clipboard_read",
            "description": "Read the current contents of the clipboard.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clipboard_write",
            "description": "Copy text to the clipboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to copy to clipboard"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_csv",
            "description": "Read and display contents of a CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the CSV file"},
                    "max_rows": {"type": "integer", "description": "Maximum rows to show (default 50)"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_csv",
            "description": "Analyze a CSV file: show number of rows, column names, and a sample row.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the CSV file"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_json",
            "description": "Read and display contents of a JSON file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the JSON file"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_pdf",
            "description": "Extract text from a PDF file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the PDF file"},
                    "max_pages": {"type": "integer", "description": "Maximum pages to read (default 10)"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and return its output. Use for file system operations, running scripts, checking system state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds (default 30)"},
                },
                "required": ["command"],
            },
        },
    },
]

_TOOL_MAP = {
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "add_note": add_note,
    "list_notes": list_notes,
    "run_command": run_command,
    "edit_text": edit_text,
    "write_email": write_email,
    "check_spelling": check_spelling,
    "translate_text": translate_text,
    "summarize_text": summarize_text,
    "generate_code": generate_code,
    "calculate": calculate,
    "clipboard_read": clipboard_read,
    "clipboard_write": clipboard_write,
    "read_csv": read_csv,
    "analyze_csv": analyze_csv,
    "read_json": read_json,
    "read_pdf": read_pdf,
}


class ToolRegistry:
    def get_tool_definitions(self) -> list:
        return TOOL_DEFINITIONS

    def call(self, name: str, arguments: dict) -> str:
        if name not in _TOOL_MAP:
            return f"Error: unknown tool '{name}'"
        try:
            return _TOOL_MAP[name](**arguments)
        except Exception as e:
            return f"Tool error: {e}"
