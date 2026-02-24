# Local Agent

> [English](#english) | [Русский](#русский)

---

## English

A local AI agent powered by [Ollama](https://ollama.com) with tool calling support. Runs entirely on your own hardware — no cloud, no API keys.

### Features

- Web search via DuckDuckGo
- File read/write and search
- Shell command execution
- Task and note management
- Clipboard read/write
- CSV, JSON, PDF reading
- Text tools: translate, summarize, generate code, check spelling

### Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally or on a network host
- A model with tool calling support (e.g. `qwen2.5:7b-instruct`)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `config.py` to set your Ollama address and model:

```python
OLLAMA_URL = "http://192.168.31.190:11434/api/chat"
MODEL = "qwen2.5:7b-instruct-q4_K_M"
```

### Usage

```bash
python main.py
```

Type your request in natural language. The agent will use tools automatically when needed. Type `exit` or press `Ctrl+C` to quit.

### Project Structure

```
local-agent/
├── config.py          # Ollama URL and model settings
├── agent.py           # Main agent loop
├── main.py            # Entry point (REPL)
├── ollama_client.py   # Ollama HTTP client
├── tool_registry.py   # Tool definitions and dispatch
└── tools/
    ├── web_search.py
    ├── file_ops.py
    ├── shell.py
    ├── tasks.py
    ├── clipboard.py
    ├── data_tools.py
    ├── text_tools.py
    └── pdf_reader.py
```

---

## Русский

Локальный AI-агент на базе [Ollama](https://ollama.com) с поддержкой вызова инструментов. Работает полностью на своём железе — без облака и API-ключей.

### Возможности

- Поиск в интернете через DuckDuckGo
- Чтение/запись файлов и поиск по содержимому
- Выполнение команд в терминале
- Управление задачами и заметками
- Работа с буфером обмена
- Чтение CSV, JSON, PDF
- Текстовые инструменты: перевод, резюме, генерация кода, проверка орфографии

### Требования

- Python 3.10+
- [Ollama](https://ollama.com) запущенный локально или на сетевом хосте
- Модель с поддержкой tool calling (например `qwen2.5:7b-instruct`)

### Установка

```bash
pip install -r requirements.txt
```

### Настройка

Отредактируй `config.py` — укажи адрес Ollama и имя модели:

```python
OLLAMA_URL = "http://192.168.31.190:11434/api/chat"
MODEL = "qwen2.5:7b-instruct-q4_K_M"
```

### Запуск

```bash
python main.py
```

Вводи запросы на естественном языке. Агент сам решает, какие инструменты использовать. Для выхода введи `exit` или нажми `Ctrl+C`.

### Структура проекта

```
local-agent/
├── config.py          # Адрес Ollama и название модели
├── agent.py           # Основной цикл агента
├── main.py            # Точка входа (REPL)
├── ollama_client.py   # HTTP-клиент для Ollama
├── tool_registry.py   # Описание и вызов инструментов
└── tools/
    ├── web_search.py
    ├── file_ops.py
    ├── shell.py
    ├── tasks.py
    ├── clipboard.py
    ├── data_tools.py
    ├── text_tools.py
    └── pdf_reader.py
```
