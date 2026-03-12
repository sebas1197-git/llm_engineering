from fpdf import FPDF
import os

FONT_DIR = "C:/Windows/Fonts"

class DocPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial",   "",   f"{FONT_DIR}/arial.ttf")
        self.add_font("Arial",   "B",  f"{FONT_DIR}/arialbd.ttf")
        self.add_font("Arial",   "I",  f"{FONT_DIR}/ariali.ttf")
        self.add_font("Arial",   "BI", f"{FONT_DIR}/arialbi.ttf")
        self.add_font("CourierU", "",  f"{FONT_DIR}/cour.ttf")
        self.add_font("CourierU", "B", f"{FONT_DIR}/courbd.ttf")

    def header(self):
        self.set_font("Arial", "B", 10)
        self.set_fill_color(20, 40, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 9, "Week 2 Exercise \u2013 Python Technical Q&A Assistant \u2013 Implementation Guide", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        self.ln(2)

    def footer(self):
        self.set_y(-14)
        self.set_font("Arial", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def part_title(self, title, subtitle=""):
        self.set_font("Arial", "B", 15)
        self.set_fill_color(20, 60, 140)
        self.set_text_color(255, 255, 255)
        self.cell(0, 11, title, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        if subtitle:
            self.set_font("Arial", "I", 10)
            self.set_fill_color(210, 222, 248)
            self.set_text_color(25, 50, 110)
            self.cell(0, 7, subtitle, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def cell_title(self, label):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(235, 241, 255)
        self.set_text_color(20, 60, 140)
        self.set_draw_color(160, 185, 230)
        self.cell(0, 8, f"  {label}", border="LB", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.ln(2)

    def section(self, title):
        self.set_font("Arial", "B", 10.5)
        self.set_text_color(40, 90, 170)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text, indent=6):
        self.set_font("Arial", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 6, f"\u2022  {text}")
        self.set_x(self.l_margin)

    def code(self, src):
        self.set_font("CourierU", "", 8.2)
        self.set_fill_color(242, 244, 248)
        self.set_draw_color(185, 195, 215)
        self.multi_cell(0, 5.2, src, fill=True, border=1)
        self.set_font("Arial", "", 10)
        self.set_draw_color(0, 0, 0)
        self.ln(2)

    def note(self, text, color=(255, 243, 205)):
        self.set_fill_color(*color)
        self.set_font("Arial", "I", 9.5)
        self.multi_cell(0, 6, text, fill=True)
        self.set_font("Arial", "", 10)
        self.ln(2)

    def label_value(self, label, value):
        self.set_font("Arial", "B", 10)
        self.cell(38, 6, label + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, value)
        self.ln(1)

    # Fixed-height table row helper
    def table_row(self, cols, widths, line_h, fill, header=False):
        color = (210, 222, 248) if header else ((235, 241, 255) if fill else (255, 255, 255))
        self.set_fill_color(*color)
        self.set_font("Arial", "B" if header else "", 8.5)
        self.set_text_color(20, 50, 120 if header else 0)

        x_start = self.l_margin
        y_start = self.get_y()

        # Measure tallest cell
        max_lines = 1
        for text, w in zip(cols, widths):
            lines = self.multi_cell(w, line_h, text, border=0, fill=False, dry_run=True, output="LINES")
            max_lines = max(max_lines, len(lines))
        row_h = max_lines * line_h

        if y_start + row_h > self.page_break_trigger:
            self.add_page()
            y_start = self.get_y()

        for i, (text, w) in enumerate(zip(cols, widths)):
            self.set_xy(x_start + sum(widths[:i]), y_start)
            if i == len(cols) - 1:
                self.multi_cell(w, line_h, text, border=1, fill=True, align="L")
            else:
                self.cell(w, row_h, text, border=1, fill=True, align="L")

        self.set_xy(x_start, y_start + row_h)
        self.set_text_color(0, 0, 0)


# ─── BUILD PDF ────────────────────────────────────────────────────────────────
pdf = DocPDF()
pdf.set_auto_page_break(auto=True, margin=14)
pdf.add_page()

# ── COVER ─────────────────────────────────────────────────────────────────────
pdf.set_font("Arial", "B", 22)
pdf.set_text_color(20, 40, 80)
pdf.ln(5)
pdf.cell(0, 13, "Week 2 Exercise", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Arial", "B", 15)
pdf.set_text_color(20, 80, 160)
pdf.cell(0, 9, "Python Technical Q&A Assistant", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Arial", "I", 11)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 7, "Implementation Guide \u2013 All 10 Notebook Cells", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_text_color(0, 0, 0)
pdf.ln(5)

pdf.set_fill_color(230, 238, 255)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 6,
    "This document is a complete implementation reference for the Week 2 end-of-week exercise. "
    "The exercise extends the Week 1 technical question/answerer into a full-featured AI assistant "
    "with a Gradio UI, streaming, model switching, SQLite-backed tool calling, and bonus TTS audio output.",
    fill=True)
pdf.ln(6)

# Feature overview table
pdf.set_font("Arial", "B", 10)
pdf.set_text_color(20, 60, 140)
pdf.cell(0, 7, "Features implemented", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)
features = [
    ("Feature", "Details"),
    ("Gradio Chat UI",      "gr.ChatInterface with model dropdown + example questions"),
    ("Streaming",           "Generator-based chat() with yield; token-by-token display"),
    ("System prompt",       "Expert Python tutor persona; tells model about snippet tools"),
    ("Model switching",     "GPT (gpt-4.1-mini) via OpenAI API  /  Ollama (llama3.2) local"),
    ("Tool calling",        "3 tools: save_snippet, get_snippet, list_snippets (GPT only)"),
    ("SQLite persistence",  "tech_qa.db stores named code snippets across sessions"),
    ("Bonus: TTS audio",    "gr.Blocks UI with gr.Audio; openai.audio.speech.create (onyx voice)"),
]
for i, row in enumerate(features):
    pdf.table_row(list(row), [70, 112], 6.5, fill=(i % 2 == 0), header=(i == 0))
pdf.ln(5)

# ═══════════════════════════════════════════════════════════════════════════════
# ARCHITECTURE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.part_title("Architecture Overview", "How all components connect")

pdf.section("Data & Control Flow")
pdf.body(
    "The notebook is structured as a linear sequence of cells. Each cell builds on the previous, "
    "so they must be run in order. The two UI cells (9 and 10) each launch a separate Gradio server.")

pdf.body("Main flow for Cell 9 (Chat UI):")
pdf.bullet("User types a question and selects a model in the Gradio UI")
pdf.bullet("chat(message, history, model) is called by Gradio")
pdf.bullet("The correct client (OpenAI or Ollama) and model ID are chosen from the dropdown value")
pdf.bullet("A messages list is built: [system] + history + [user message]")
pdf.bullet("If GPT: first API call includes tools=[...]; if Ollama: no tools")
pdf.bullet("while finish_reason == 'tool_calls': execute tools, append results, call API again")
pdf.bullet("Once a plain text response is ready, re-call with stream=True and yield tokens")
pdf.ln(2)

pdf.body("Main flow for Cell 10 (Audio UI):")
pdf.bullet("User submits message \u2192 add_user_message() appends it to chatbot history")
pdf.bullet(".then() fires chat_with_audio(history) \u2013 history already contains the user message")
pdf.bullet("Same tool-calling loop as above, but synchronous (no streaming)")
pdf.bullet("Final reply text is stripped of markdown, passed to talker() \u2192 TTS audio bytes")
pdf.bullet("Gradio returns updated history + audio bytes \u2192 gr.Audio plays automatically")
pdf.ln(3)

pdf.section("Why tools are GPT-only")
pdf.note(
    "Ollama's tool calling support varies by model and is unreliable for llama3.2. "
    "The chat() callback uses a simple flag (use_tools = 'GPT' in model) to skip "
    "the tool schema when routing to Ollama, keeping it as a clean streaming-only path.",
    color=(255, 235, 210))

pdf.section("Key design decisions")
pdf.bullet("TOOL_HANDLERS dispatch registry: adding a new tool only requires one dict entry + one schema")
pdf.bullet("handle_tool_calls() is shared between both UI cells (no duplication)")
pdf.bullet("system_message is a global so it's available to both chat() and chat_with_audio()")
pdf.bullet("lines=1 on the Textbox in Cell 10 so Enter submits instead of inserting a newline")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL-BY-CELL REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.part_title("Cell-by-Cell Implementation Reference")

# ── CELL 1 ──
pdf.cell_title("Cell 1 \u2013 Imports")
pdf.body("All dependencies imported at the top. No setup required beyond the course virtualenv.")
pdf.code(
    "import os\n"
    "import json\n"
    "import sqlite3\n"
    "from dotenv import load_dotenv\n"
    "from openai import OpenAI\n"
    "import gradio as gr")
pdf.label_value("os",         "Reading OPENAI_API_KEY from environment")
pdf.label_value("json",       "Parsing tool call arguments (json.loads)")
pdf.label_value("sqlite3",    "Persistent snippet database")
pdf.label_value("dotenv",     "Loading .env without restarting the kernel")
pdf.label_value("OpenAI",     "Client for both OpenAI and Ollama (OpenAI-compatible endpoint)")
pdf.label_value("gradio",     "UI framework for both Chat and Audio interfaces")
pdf.ln(2)

# ── CELL 2 ──
pdf.cell_title("Cell 2 \u2013 Configuration & Clients")
pdf.body(
    "Constants and both API clients are defined here. "
    "Ollama uses the same OpenAI Python client pointed at localhost:11434 \u2013 "
    "the OpenAI-compatible endpoint pattern from Week 2 Day 2.")
pdf.code(
    'load_dotenv(override=True)\n\n'
    'GPT_MODEL    = "gpt-4.1-mini"\n'
    'OLLAMA_MODEL = "llama3.2"\n'
    'DB           = "tech_qa.db"\n\n'
    'openai_client = OpenAI()\n'
    'ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")')
pdf.note("override=True forces load_dotenv to re-read .env even if the variable is already set in the environment, which avoids stale values during iterative notebook development.")

# ── CELL 3 ──
pdf.cell_title("Cell 3 \u2013 SQLite Database Init")
pdf.body(
    "Creates tech_qa.db with a single table on first run. "
    "IF NOT EXISTS makes the call idempotent \u2013 safe to re-run the cell without data loss.")
pdf.code(
    'def init_db():\n'
    '    with sqlite3.connect(DB) as conn:\n'
    '        conn.execute("""\n'
    '            CREATE TABLE IF NOT EXISTS snippets (\n'
    '                name        TEXT PRIMARY KEY,\n'
    '                code        TEXT NOT NULL,\n'
    '                description TEXT DEFAULT \'\'\n'
    '            )\n'
    '        """)\n'
    '        conn.commit()\n\n'
    'init_db()')
pdf.label_value("name",        "Primary key \u2013 case-folded to lowercase on write")
pdf.label_value("code",        "The Python source code to store")
pdf.label_value("description", "Optional one-line summary; shown in list_snippets()")
pdf.ln(2)

# ── CELL 4 ──
pdf.add_page()
pdf.cell_title("Cell 4 \u2013 Tool Functions")
pdf.body(
    "Three Python functions that form the backend of the snippet library. "
    "Each uses a context-manager connection and parameterised queries (? placeholders) "
    "to prevent SQL injection.")

pdf.section("save_snippet(name, code, description)")
pdf.body("Upserts a snippet. If the name already exists, both code and description are overwritten.")
pdf.code(
    'def save_snippet(name: str, code: str, description: str = "") -> str:\n'
    '    print(f"TOOL: save_snippet(name={name!r})", flush=True)\n'
    '    with sqlite3.connect(DB) as conn:\n'
    '        conn.execute(\n'
    '            "INSERT INTO snippets (name, code, description) VALUES (?, ?, ?)"\n'
    '            " ON CONFLICT(name) DO UPDATE SET code=excluded.code,"\n'
    '            " description=excluded.description",\n'
    '            (name.lower(), code, description)\n'
    '        )\n'
    '        conn.commit()\n'
    '    return f"Snippet \'{name}\' saved successfully."')

pdf.section("get_snippet(name)")
pdf.body("Retrieves code and description for a named snippet. Returns a formatted markdown string.")
pdf.code(
    'def get_snippet(name: str) -> str:\n'
    '    with sqlite3.connect(DB) as conn:\n'
    '        row = conn.execute(\n'
    '            "SELECT code, description FROM snippets WHERE name = ?",\n'
    '            (name.lower(),)\n'
    '        ).fetchone()\n'
    '    if row:\n'
    '        code, desc = row\n'
    '        result = f"**{name}**"\n'
    '        if desc:\n'
    '            result += f" \u2013 {desc}"\n'
    '        result += f"\\n```python\\n{code}\\n```"\n'
    '        return result\n'
    '    return f"No snippet found with name \'{name}\'."')

pdf.section("list_snippets()")
pdf.body("Returns a markdown bullet list of all saved snippet names and descriptions.")
pdf.code(
    'def list_snippets() -> str:\n'
    '    with sqlite3.connect(DB) as conn:\n'
    '        rows = conn.execute(\n'
    '            "SELECT name, description FROM snippets ORDER BY name"\n'
    '        ).fetchall()\n'
    '    if not rows:\n'
    '        return "No snippets saved yet."\n'
    '    lines = [f"- **{name}**: {desc or \'(no description)\'}" for name, desc in rows]\n'
    '    return "Saved snippets:\\n" + "\\n".join(lines)')

# ── CELL 5 ──
pdf.add_page()
pdf.cell_title("Cell 5 \u2013 Tool Schemas & Dispatch Registry")
pdf.body(
    "Each tool is described as a JSON schema so the LLM knows its name, purpose, and parameters. "
    "The TOOL_HANDLERS registry maps tool names to lambda wrappers, keeping handle_tool_calls() "
    "generic and easy to extend.")

pdf.section("Tool Schema Structure (same format as Day 4)")
pdf.code(
    'save_snippet_function = {\n'
    '    "name": "save_snippet",\n'
    '    "description": "Save a named Python code snippet to the persistent library.",\n'
    '    "parameters": {\n'
    '        "type": "object",\n'
    '        "properties": {\n'
    '            "name":        {"type": "string", "description": "Short unique identifier"},\n'
    '            "code":        {"type": "string", "description": "The Python code to save"},\n'
    '            "description": {"type": "string", "description": "Optional one-line summary"}\n'
    '        },\n'
    '        "required": ["name", "code"],\n'
    '        "additionalProperties": False\n'
    '    }\n'
    '}')

pdf.section("Tools List & Dispatch Registry")
pdf.code(
    'tools = [\n'
    '    {"type": "function", "function": save_snippet_function},\n'
    '    {"type": "function", "function": get_snippet_function},\n'
    '    {"type": "function", "function": list_snippets_function},\n'
    ']\n\n'
    'TOOL_HANDLERS = {\n'
    '    "save_snippet":  lambda a: save_snippet(a["name"], a["code"], a.get("description", "")),\n'
    '    "get_snippet":   lambda a: get_snippet(a["name"]),\n'
    '    "list_snippets": lambda a: list_snippets(),\n'
    '}')
pdf.note(
    "The dispatch registry pattern means handle_tool_calls() never needs to be modified "
    "when adding new tools \u2013 only this dict and a new schema need updating.")

# ── CELL 6 ──
pdf.cell_title("Cell 6 \u2013 System Prompt")
pdf.body(
    "The system message defines the assistant's persona and teaches it how to use its tools. "
    "Explicitly telling the model when to call each tool (one-shot instruction) "
    "dramatically improves reliability compared to hoping the model infers it.")
pdf.code(
    'system_message = """\n'
    'You are an expert Python and programming tutor with deep knowledge of:\n'
    '- Python fundamentals, idioms, and best practices\n'
    '- Data structures, algorithms, and design patterns\n'
    '- The Python standard library and popular packages\n\n'
    'Your style:\n'
    '- Give clear, accurate explanations with concrete examples\n'
    '- Always use markdown formatting with fenced code blocks for code\n'
    '- Break down complex topics step by step\n\n'
    'You have access to a persistent code snippet library:\n'
    '- save_snippet  \u2013 when a user asks to save something, call this immediately\n'
    '- list_snippets \u2013 when asked what snippets are available\n'
    '- get_snippet   \u2013 when asked to show a specific snippet\n'
    '""".strip()')

# ── CELL 7 ──
pdf.add_page()
pdf.cell_title("Cell 7 \u2013 handle_tool_calls()")
pdf.body(
    "Iterates over all tool calls in a single assistant message, dispatches each to the correct "
    "handler via TOOL_HANDLERS, and returns a list of tool-role messages to append to the conversation. "
    "Error handling ensures one failing tool doesn't crash the whole response.")
pdf.code(
    'def handle_tool_calls(message):\n'
    '    responses = []\n'
    '    for tool_call in message.tool_calls:\n'
    '        name      = tool_call.function.name\n'
    '        arguments = json.loads(tool_call.function.arguments)\n'
    '        try:\n'
    '            handler = TOOL_HANDLERS.get(name)\n'
    '            result  = handler(arguments) if handler else f"Unknown tool: {name}"\n'
    '        except Exception as e:\n'
    '            result = f"Error calling {name}: {e}"\n'
    '        responses.append({\n'
    '            "role":         "tool",\n'
    '            "content":      str(result),\n'
    '            "tool_call_id": tool_call.id,\n'
    '        })\n'
    '    return responses')

pdf.section("Message structure after a tool call cycle")
pdf.body(
    "After the while loop in chat(), the messages list looks like this (simplified):\n"
    "[system, user, assistant(tool_calls=[...]), tool(result), assistant(final text)]")

# ── CELL 8 ──
pdf.cell_title("Cell 8 \u2013 chat() Callback")
pdf.body(
    "The central callback wiring everything together. "
    "Accepts three arguments: the new message, the Gradio conversation history, "
    "and the selected model from the dropdown.")

pdf.section("Model routing")
pdf.code(
    'use_gpt   = "GPT" in model\n'
    'client    = openai_client if use_gpt else ollama_client\n'
    'model_id  = GPT_MODEL     if use_gpt else OLLAMA_MODEL\n'
    'use_tools = use_gpt   # Ollama tool calling unreliable for llama3.2')

pdf.section("Tool calling loop + streaming (full function)")
pdf.code(
    'def chat(message, history, model):\n'
    '    use_gpt   = "GPT" in model\n'
    '    client    = openai_client if use_gpt else ollama_client\n'
    '    model_id  = GPT_MODEL     if use_gpt else OLLAMA_MODEL\n'
    '    use_tools = use_gpt\n\n'
    '    messages = (\n'
    '        [{"role": "system", "content": system_message}]\n'
    '        + [{"role": h["role"], "content": h["content"]} for h in history]\n'
    '        + [{"role": "user",   "content": message}]\n'
    '    )\n\n'
    '    kwargs   = {"tools": tools} if use_tools else {}\n'
    '    response = client.chat.completions.create(\n'
    '        model=model_id, messages=messages, **kwargs)\n\n'
    '    while use_tools and response.choices[0].finish_reason == "tool_calls":\n'
    '        tool_msg     = response.choices[0].message\n'
    '        tool_results = handle_tool_calls(tool_msg)\n'
    '        messages.append(tool_msg)\n'
    '        messages.extend(tool_results)\n'
    '        response = client.chat.completions.create(\n'
    '            model=model_id, messages=messages, **kwargs)\n\n'
    '    stream = client.chat.completions.create(\n'
    '        model=model_id, messages=messages, stream=True)\n'
    '    result = ""\n'
    '    for chunk in stream:\n'
    '        result += chunk.choices[0].delta.content or ""\n'
    '        yield result')

pdf.note(
    "Why two API calls for the streaming case? The tool-calling loop uses a regular "
    "(non-streaming) call so we can check finish_reason. Once tools are resolved, "
    "a second call with stream=True gives us the token-by-token display.",
    color=(230, 248, 230))

# ── CELL 9 ──
pdf.add_page()
pdf.cell_title("Cell 9 \u2013 Gradio Chat UI (gr.ChatInterface)")
pdf.body(
    "Wraps the chat() callback in Gradio's built-in chat interface. "
    "additional_inputs injects the model dropdown as a third argument to chat().")
pdf.code(
    'model_dropdown = gr.Dropdown(\n'
    '    choices=["GPT (gpt-4.1-mini)", "Ollama (llama3.2)"],\n'
    '    value="GPT (gpt-4.1-mini)",\n'
    '    label="Model",\n'
    '    info="GPT supports tool calling. Ollama is free & local."\n'
    ')\n\n'
    'gr.ChatInterface(\n'
    '    fn=chat,\n'
    '    type="messages",\n'
    '    title="Python Technical Q&A Assistant",\n'
    '    additional_inputs=[model_dropdown],\n'
    '    examples=[\n'
    '        ["Explain what `yield from` does in Python.", "GPT (gpt-4.1-mini)"],\n'
    '        ["Show me a FizzBuzz and save it as \'fizzbuzz\'.", "GPT (gpt-4.1-mini)"],\n'
    '        ["What snippets do I have saved?", "GPT (gpt-4.1-mini)"],\n'
    '        ["Explain decorators.", "Ollama (llama3.2)"],\n'
    '    ],\n'
    '    flagging_mode="never",\n'
    ').launch(inbrowser=True)')

pdf.section("Key parameters")
rows9 = [
    ("Parameter", "Value", "Purpose"),
    ("type",              "'messages'",         "History is list of {role,content} dicts \u2013 matches API format directly"),
    ("additional_inputs", "[model_dropdown]",   "Appends dropdown value as 3rd arg to chat()"),
    ("examples",          "List of [msg,model]","Pre-fills input + dropdown; clickable in the UI"),
    ("flagging_mode",     "'never'",             "Disables the feedback/flag button (not needed here)"),
]
for i, row in enumerate(rows9):
    pdf.table_row(list(row), [40, 45, 97], 6.5, fill=(i % 2 == 0), header=(i == 0))
pdf.ln(4)

# ── CELL 10 ──
pdf.cell_title("Cell 10 \u2013 Bonus Audio UI (gr.Blocks + TTS)")
pdf.body(
    "A second, more advanced interface using gr.Blocks for a custom layout. "
    "Adds spoken audio output alongside the chat using OpenAI's TTS endpoint.")

pdf.section("talker() \u2013 Text to Speech")
pdf.code(
    'def talker(text: str) -> bytes:\n'
    '    response = openai_client.audio.speech.create(\n'
    '        model="gpt-4o-mini-tts",\n'
    '        voice="onyx",       # alternatives: alloy, coral, echo, fable, nova, shimmer\n'
    '        input=text[:4096]   # cap to avoid very long TTS calls\n'
    '    )\n'
    '    return response.content  # raw audio bytes')

pdf.section("chat_with_audio(history) \u2013 Synchronous with TTS")
pdf.body(
    "Unlike chat(), this callback is NOT a generator. "
    "It runs the full tool loop, gets the complete reply, converts it to audio, "
    "and returns both in one shot.")
pdf.code(
    'def chat_with_audio(history):\n'
    '    # history already contains the user message (added by add_user_message)\n'
    '    messages = (\n'
    '        [{"role": "system", "content": system_message}]\n'
    '        + [{"role": h["role"], "content": h["content"]} for h in history]\n'
    '    )\n'
    '    response = openai_client.chat.completions.create(\n'
    '        model=GPT_MODEL, messages=messages, tools=tools)\n\n'
    '    while response.choices[0].finish_reason == "tool_calls":\n'
    '        tool_msg     = response.choices[0].message\n'
    '        tool_results = handle_tool_calls(tool_msg)\n'
    '        messages.append(tool_msg)\n'
    '        messages.extend(tool_results)\n'
    '        response = openai_client.chat.completions.create(\n'
    '            model=GPT_MODEL, messages=messages, tools=tools)\n\n'
    '    reply      = response.choices[0].message.content\n'
    '    history    = history + [{"role": "assistant", "content": reply}]\n'
    '    plain_text = reply.replace("```python","").replace("```","")  # strip md for TTS\n'
    '    audio      = talker(plain_text)\n'
    '    return history, audio')

pdf.section("gr.Blocks Layout & Event Wiring")
pdf.body(
    "The .submit()/.click() \u2192 .then() chain runs two callbacks in sequence: "
    "first append the user message, then call the LLM + TTS.")
pdf.code(
    'with gr.Blocks() as audio_ui:\n'
    '    chatbot      = gr.Chatbot(height=450, type="messages")\n'
    '    audio_output = gr.Audio(autoplay=True)\n'
    '    msg_box      = gr.Textbox(lines=1, ...)  # lines=1: Enter submits\n'
    '    send_btn     = gr.Button("Send", variant="primary")\n\n'
    '    trigger   = dict(fn=add_user_message,\n'
    '                     inputs=[msg_box, chatbot], outputs=[msg_box, chatbot])\n'
    '    followup  = dict(fn=chat_with_audio,\n'
    '                     inputs=chatbot, outputs=[chatbot, audio_output])\n\n'
    '    msg_box.submit(**trigger).then(**followup)  # Enter key\n'
    '    send_btn.click(**trigger).then(**followup)  # Send button\n\n'
    'audio_ui.launch(inbrowser=True)')

pdf.note(
    "lines=1 is critical: Gradio treats Enter as a newline in multi-line textboxes. "
    "Setting lines=1 restores the submit-on-Enter behaviour. "
    "The Send button provides a fallback for touch/mobile users.",
    color=(255, 235, 210))

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.part_title("Quick Reference \u2013 All Cells at a Glance")

ref_rows = [
    ("Cell", "Name", "Key Output / Purpose"),
    ("1",  "Imports",                   "os, json, sqlite3, OpenAI, gradio"),
    ("2",  "Config & Clients",          "GPT_MODEL, OLLAMA_MODEL, DB, openai_client, ollama_client"),
    ("3",  "SQLite Init",               "tech_qa.db with snippets table (name PK, code, description)"),
    ("4",  "Tool Functions",            "save_snippet(), get_snippet(), list_snippets() \u2013 all SQLite-backed"),
    ("5",  "Schemas & Registry",        "3 JSON schemas + TOOL_HANDLERS dict + tools list"),
    ("6",  "System Prompt",             "Expert Python tutor persona; explicit tool-use instructions"),
    ("7",  "handle_tool_calls()",       "Dispatch registry loop; returns list of tool-role messages"),
    ("8",  "chat() Callback",           "Model routing + tool loop + streaming yield"),
    ("9",  "Gradio Chat UI",            "gr.ChatInterface with dropdown, streaming, examples"),
    ("10", "Audio UI (Bonus)",          "gr.Blocks + TTS; .then() event chain; lines=1 fix"),
]
for i, row in enumerate(ref_rows):
    pdf.table_row(list(row), [14, 46, 122], 6.5, fill=(i % 2 == 0), header=(i == 0))

pdf.ln(6)
pdf.part_title("Troubleshooting & Common Issues")

issues = [
    ("UserWarning: Expected 2 args, received 1",
     "chat_with_audio was defined as (message, history) but Gradio passes only history via .then(). "
     "Fix: change signature to (history) only \u2013 the user message is already in history."),
    ("Enter creates newline instead of sending",
     "gr.Textbox with lines>1 treats Enter as newline. Fix: set lines=1. "
     "Also add a gr.Button('Send') as fallback."),
    ("Ollama tool calls not working",
     "llama3.2 tool calling is unreliable. Tools are intentionally disabled for Ollama "
     "via the use_tools = use_gpt flag in chat()."),
    ("'No API key' error for OpenAI",
     "Run load_dotenv(override=True) in Cell 2 after saving .env. "
     "Check the key starts with sk-proj-."),
    ("Ollama not responding",
     "Run 'ollama serve' in a terminal. Visit http://localhost:11434 to confirm it's running. "
     "Pull the model first: ollama pull llama3.2"),
    ("TTS audio not playing",
     "The gr.Audio component needs autoplay=True. Some browsers block autoplay \u2013 "
     "click the play button manually if needed."),
]
for label, detail in issues:
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(160, 40, 40)
    pdf.multi_cell(0, 6, f"[!] {label}")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 9.5)
    pdf.set_x(pdf.l_margin + 6)
    pdf.multi_cell(0, 6, detail)
    pdf.ln(2)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week2_exercise_implementation.pdf")
pdf.output(out_path)
print(f"PDF saved to: {out_path}")
