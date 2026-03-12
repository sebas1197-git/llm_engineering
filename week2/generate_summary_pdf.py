from fpdf import FPDF
import os

FONT_DIR = "C:/Windows/Fonts"

class SummaryPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial", "",   f"{FONT_DIR}/arial.ttf")
        self.add_font("Arial", "B",  f"{FONT_DIR}/arialbd.ttf")
        self.add_font("Arial", "I",  f"{FONT_DIR}/ariali.ttf")
        self.add_font("Arial", "BI", f"{FONT_DIR}/arialbi.ttf")

    def header(self):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(20, 40, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "LLM Engineering \u2013 Week 2 Key Concepts", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title, subtitle=""):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(20, 80, 160)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        if subtitle:
            self.set_font("Arial", "I", 10)
            self.set_fill_color(210, 225, 250)
            self.set_text_color(30, 50, 100)
            self.cell(0, 7, subtitle, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.set_text_color(20, 70, 150)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def bullet(self, text, indent=8):
        self.set_font("Arial", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 6, f"\u2022  {text}")
        self.set_x(self.l_margin)

    def code_block(self, code):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(240, 242, 246)
        self.set_draw_color(180, 185, 200)
        self.multi_cell(0, 5.5, code, fill=True, border=1)
        self.set_font("Arial", "", 10)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def note_box(self, text, color=(255, 243, 205)):
        self.set_fill_color(*color)
        self.set_font("Arial", "I", 9.5)
        self.multi_cell(0, 6, text, fill=True)
        self.set_font("Arial", "", 10)
        self.ln(2)


pdf = SummaryPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ── COVER ────────────────────────────────────────────────────────────────────
pdf.set_font("Arial", "B", 22)
pdf.set_text_color(20, 40, 80)
pdf.ln(6)
pdf.cell(0, 13, "LLM Engineering \u2013 Week 2", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Arial", "B", 15)
pdf.set_text_color(20, 80, 160)
pdf.cell(0, 9, "Key Concepts Summary: Days 1 \u2013 5", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_text_color(0, 0, 0)
pdf.ln(5)
pdf.set_font("Arial", "", 10)
pdf.set_fill_color(230, 238, 255)
pdf.multi_cell(0, 6,
    "This document summarises the most important concepts, patterns and code techniques "
    "introduced across all five days of Week 2 of the LLM Engineering course. "
    "Topics progress from multi-provider API access and UI building through "
    "conversational chatbots, tool calling, and finally multi-modal AI assistants.",
    fill=True)
pdf.ln(8)

# ════════════════════════════════════════════════════════════════════════════
# DAY 1
# ════════════════════════════════════════════════════════════════════════════
pdf.chapter_title("Day 1 \u2013 Frontier Model APIs & the Provider Ecosystem",
                  "Multi-provider connections, reasoning effort, LiteLLM, prompt caching & adversarial chatbots")

pdf.section_title("1. Connecting to Every Major Provider")
pdf.body_text(
    "Because all major LLM providers now expose an OpenAI-compatible endpoint, "
    "you can connect to all of them using a single pattern: "
    "swap base_url and api_key on the OpenAI Python client.")
pdf.code_block(
    'from openai import OpenAI\n\n'
    'openai    = OpenAI()   # default: api.openai.com\n'
    'anthropic = OpenAI(api_key=anthropic_key, base_url="https://api.anthropic.com/v1/")\n'
    'gemini    = OpenAI(api_key=google_key,    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")\n'
    'deepseek  = OpenAI(api_key=deepseek_key,  base_url="https://api.deepseek.com")\n'
    'groq      = OpenAI(api_key=groq_key,      base_url="https://api.groq.com/openai/v1")\n'
    'grok      = OpenAI(api_key=grok_key,      base_url="https://api.x.ai/v1")\n'
    'ollama    = OpenAI(api_key="ollama",       base_url="http://localhost:11434/v1")')

pdf.section_title("2. Training-Time vs Inference-Time Scaling")
pdf.body_text(
    "Some models (e.g. GPT-5, o-series) support a reasoning_effort parameter "
    "that controls how much 'thinking' the model does at inference time. "
    "Higher effort = slower but more accurate; useful for hard logical puzzles.")
pdf.code_block(
    '# Minimal reasoning - fast & cheap\n'
    'openai.chat.completions.create(model="gpt-5-nano", messages=puzzle, reasoning_effort="minimal")\n\n'
    '# Full reasoning power\n'
    'openai.chat.completions.create(model="gpt-5", messages=puzzle)')

pdf.section_title("3. Native Client Libraries")
pdf.body_text("For providers that have their own SDKs, you can also use them directly:")
pdf.code_block(
    '# Google native SDK\n'
    'from google import genai\n'
    'client = genai.Client()\n'
    'response = client.models.generate_content(model="gemini-2.5-flash-lite", contents="...")\n\n'
    '# Anthropic native SDK\n'
    'from anthropic import Anthropic\n'
    'client = Anthropic()\n'
    'response = client.messages.create(model="claude-sonnet-4-5-20250929",\n'
    '    messages=[{"role":"user","content":"..."}], max_tokens=100)')

pdf.section_title("4. OpenRouter \u2013 Unified Interface for All Models")
pdf.body_text(
    "OpenRouter (openrouter.ai) provides a single API key and endpoint that "
    "proxies dozens of models. Useful when you want to switch providers without "
    "changing infrastructure.")
pdf.code_block(
    'openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_key)\n'
    'response = openrouter.chat.completions.create(model="z-ai/glm-4.5", messages=[...])')

pdf.section_title("5. LangChain \u2013 Heavyweight Framework")
pdf.body_text(
    "LangChain wraps LLM calls in a higher-level abstraction. "
    "The entry point for OpenAI is ChatOpenAI; responses come back as message objects.")
pdf.code_block(
    'from langchain_openai import ChatOpenAI\n'
    'llm = ChatOpenAI(model="gpt-5-mini")\n'
    'response = llm.invoke(messages)\n'
    'print(response.content)')

pdf.section_title("6. LiteLLM \u2013 Lightweight Universal Wrapper")
pdf.body_text(
    "LiteLLM is a thin, pip-installable library that provides one unified "
    "completion() call for 100+ models and exposes token usage and cost tracking.")
pdf.code_block(
    'from litellm import completion\n'
    'response = completion(model="openai/gpt-4.1", messages=[...])\n'
    'print(f"Cost: {response._hidden_params[\'response_cost\']*100:.4f} cents")')

pdf.section_title("7. Prompt Caching")
pdf.body_text(
    "All three major providers support caching repeated prompt prefixes, "
    "dramatically reducing cost for large static context (e.g. pasting a whole book).")
pdf.bullet("OpenAI  \u2013 automatic; place static content at the start of the prompt. Cached input is 4x cheaper.")
pdf.bullet("Anthropic \u2013 explicit; you mark blocks with cache_control. 25% more to prime, 10x cheaper to reuse.")
pdf.bullet("Gemini \u2013 supports both implicit and explicit caching.")
pdf.ln(2)
pdf.code_block(
    '# LiteLLM exposes cached token counts\n'
    'print(f"Cached tokens: {response.usage.prompt_tokens_details.cached_tokens}")')

pdf.section_title("8. Adversarial / Multi-Model Conversations")
pdf.body_text(
    "By replaying the full conversation history (with roles swapped) for each model, "
    "you can orchestrate a back-and-forth dialogue between two different LLMs. "
    "Each model only sees its own system prompt plus the full turn history.")
pdf.code_block(
    '# GPT sees Claude\'s messages as "user"; its own as "assistant"\n'
    'def call_gpt():\n'
    '    messages = [{"role": "system", "content": gpt_system}]\n'
    '    for gpt_turn, claude_turn in zip(gpt_messages, claude_messages):\n'
    '        messages.append({"role": "assistant", "content": gpt_turn})\n'
    '        messages.append({"role": "user",      "content": claude_turn})\n'
    '    return openai.chat.completions.create(model=gpt_model, messages=messages)\\\n'
    '                .choices[0].message.content')

# ════════════════════════════════════════════════════════════════════════════
# DAY 2
# ════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 2 \u2013 Building UIs with Gradio",
                  "gr.Interface, streaming, multi-model selector, brochure generator")

pdf.section_title("1. What Is Gradio?")
pdf.body_text(
    "Gradio is a Python library that auto-generates a web UI around any Python function. "
    "It starts a local Starlette server, builds a Svelte frontend, and wires them together. "
    "It is primarily aimed at demos, prototypes and internal tools.")
pdf.code_block(
    'import gradio as gr\n\n'
    'def shout(text):\n'
    '    return text.upper()\n\n'
    'gr.Interface(fn=shout, inputs="textbox", outputs="textbox",\n'
    '             flagging_mode="never").launch()')

pdf.section_title("2. Key gr.Interface Options")
pdf.bullet('share=True        \u2013 creates a temporary public URL via HTTP tunneling')
pdf.bullet('inbrowser=True    \u2013 opens a browser window automatically')
pdf.bullet('auth=("user","pw")\u2013 adds basic HTTP authentication')
pdf.bullet('examples=[...]    \u2013 pre-fills the UI with example inputs')
pdf.bullet('js=force_dark_mode\u2013 injects JS to force dark mode (not recommended by Gradio)')
pdf.ln(2)
pdf.code_block(
    'gr.Interface(fn=shout, inputs="textbox", outputs="textbox",\n'
    '             flagging_mode="never").launch(auth=("ed", "bananas"))')

pdf.section_title("3. Custom Input / Output Components")
pdf.body_text(
    "Instead of using string shortcuts like 'textbox', you can instantiate "
    "Gradio components directly to control labels, line counts, etc.:")
pdf.code_block(
    'msg_in  = gr.Textbox(label="Your message:", lines=7)\n'
    'msg_out = gr.Markdown(label="Response:")   # renders markdown\n\n'
    'gr.Interface(fn=message_gpt, inputs=[msg_in], outputs=[msg_out],\n'
    '             examples=["hello", "howdy"], flagging_mode="never").launch()')

pdf.section_title("4. Streaming Responses with Generators")
pdf.body_text(
    "If your callback is a Python generator (uses yield), Gradio streams the "
    "output token-by-token, giving a typewriter effect:")
pdf.code_block(
    'def stream_gpt(prompt):\n'
    '    stream = openai.chat.completions.create(\n'
    '        model="gpt-4.1-mini", messages=[...], stream=True\n'
    '    )\n'
    '    result = ""\n'
    '    for chunk in stream:\n'
    '        result += chunk.choices[0].delta.content or ""\n'
    '        yield result   # Gradio updates the UI on each yield')

pdf.section_title("5. Multi-Model Selector")
pdf.body_text(
    "You can add a Dropdown component to let users choose which model to use at runtime:")
pdf.code_block(
    'model_selector = gr.Dropdown(["GPT", "Claude"], label="Select model", value="GPT")\n\n'
    'def stream_model(prompt, model):\n'
    '    if model == "GPT":    yield from stream_gpt(prompt)\n'
    '    elif model == "Claude": yield from stream_claude(prompt)\n\n'
    'gr.Interface(fn=stream_model,\n'
    '             inputs=[gr.Textbox(lines=7), model_selector],\n'
    '             outputs=[gr.Markdown()], flagging_mode="never").launch()')

pdf.section_title("6. Practical Example \u2013 Brochure Generator UI")
pdf.note_box(
    "The Day 1 brochure pipeline (web scraper + LLM) can be wrapped in a Gradio UI "
    "with just a few lines. The user types a company name and URL, picks a model, "
    "and the brochure streams directly into a Markdown component. "
    "This pattern \u2013 wrapping an existing function in a Gradio interface \u2013 is "
    "the fastest path from notebook prototype to shareable demo.")

# ════════════════════════════════════════════════════════════════════════════
# DAY 3
# ════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 3 \u2013 Conversational AI \u2013 Building a Chatbot",
                  "gr.ChatInterface, chat callbacks, history management, persona via system prompt")

pdf.section_title("1. gr.ChatInterface")
pdf.body_text(
    "Gradio's gr.ChatInterface component creates a full chat UI with just one line. "
    "You provide a callback function with the signature chat(message, history) "
    "and Gradio handles the rest.")
pdf.code_block(
    'def chat(message, history):\n'
    '    return "Hello!"   # simplest possible callback\n\n'
    'gr.ChatInterface(fn=chat, type="messages").launch()')

pdf.section_title("2. History Format")
pdf.body_text(
    "When type='messages', Gradio passes history as a list of dicts "
    "with role and content keys \u2013 exactly the same format the LLM API expects:")
pdf.code_block(
    '# history looks like:\n'
    '# [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]\n\n'
    'def chat(message, history):\n'
    '    history = [{"role": h["role"], "content": h["content"]} for h in history]\n'
    '    messages = [{"role": "system", "content": system_message}] + history \\\n'
    '               + [{"role": "user", "content": message}]\n'
    '    response = openai.chat.completions.create(model=MODEL, messages=messages)\n'
    '    return response.choices[0].message.content')

pdf.section_title("3. Streaming Chatbot")
pdf.body_text(
    "Exactly as with gr.Interface, making the callback a generator enables streaming:")
pdf.code_block(
    'def chat(message, history):\n'
    '    messages = [{"role": "system", "content": system_message}] \\\n'
    '               + history + [{"role": "user", "content": message}]\n'
    '    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)\n'
    '    response = ""\n'
    '    for chunk in stream:\n'
    '        response += chunk.choices[0].delta.content or ""\n'
    '        yield response')

pdf.section_title("4. Controlling Persona with the System Prompt")
pdf.body_text(
    "The system message is the primary lever for shaping the chatbot's behaviour. "
    "It can encode role, tone, knowledge constraints, and business rules:")
pdf.code_block(
    'system_message = """You are a helpful assistant in a clothes store.\n'
    'Hats are 60% off; most other items are 50% off.\n'
    'Gently encourage customers toward sale items."""')
pdf.body_text("You can also mutate the system message dynamically at runtime based on message content:")
pdf.code_block(
    'def chat(message, history):\n'
    '    sys = system_message\n'
    '    if "belt" in message.lower():\n'
    '        sys += " The store does not sell belts; redirect to other items."\n'
    '    messages = [{"role": "system", "content": sys}] + history + \\\n'
    '               [{"role": "user", "content": message}]\n'
    '    ...')

pdf.section_title("5. Business Application")
pdf.note_box(
    "Conversational assistants are the most common Gen-AI use case. "
    "The pattern from Day 3 \u2013 system prompt + history + new message \u2013 "
    "is the foundation for customer support bots, onboarding assistants, "
    "internal knowledge bases, and more. "
    "Use the system prompt to encode your business context and tone.")

# ════════════════════════════════════════════════════════════════════════════
# DAY 4
# ════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 4 \u2013 Tool Calling (Function Calling)",
                  "Airline AI assistant, tool schemas, handle_tool_calls loop, SQLite integration")

pdf.section_title("1. What Is Tool Calling?")
pdf.body_text(
    "Tool calling (also known as function calling) lets you register Python functions "
    "with the LLM. When the model decides it needs to call a function to answer a question, "
    "it returns a special finish_reason='tool_calls' response instead of text. "
    "You then execute the function and feed the result back into the conversation.")
pdf.body_text("Important: the LLM never executes code directly \u2013 it only asks you to run it.")

pdf.section_title("2. Defining a Tool Schema")
pdf.body_text(
    "Each tool is described as a JSON schema dict with name, description, and parameters. "
    "This description is what helps the model decide when and how to call the function:")
pdf.code_block(
    'price_function = {\n'
    '    "name": "get_ticket_price",\n'
    '    "description": "Get the price of a return ticket to the destination city.",\n'
    '    "parameters": {\n'
    '        "type": "object",\n'
    '        "properties": {\n'
    '            "destination_city": {\n'
    '                "type": "string",\n'
    '                "description": "The city that the customer wants to travel to"\n'
    '            }\n'
    '        },\n'
    '        "required": ["destination_city"],\n'
    '        "additionalProperties": False\n'
    '    }\n'
    '}\n'
    'tools = [{"type": "function", "function": price_function}]')

pdf.section_title("3. The Tool Calling Loop")
pdf.body_text(
    "The correct pattern is a while loop: keep calling the model and executing tools "
    "until it produces a plain text response. This handles chained tool calls:")
pdf.code_block(
    'def chat(message, history):\n'
    '    messages = [{"role": "system", "content": system_message}] \\\n'
    '               + history + [{"role": "user", "content": message}]\n'
    '    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)\n\n'
    '    while response.choices[0].finish_reason == "tool_calls":\n'
    '        tool_msg  = response.choices[0].message\n'
    '        tool_results = handle_tool_calls(tool_msg)\n'
    '        messages.append(tool_msg)         # assistant\'s tool-call request\n'
    '        messages.extend(tool_results)      # our tool results\n'
    '        response = openai.chat.completions.create(\n'
    '            model=MODEL, messages=messages, tools=tools)\n\n'
    '    return response.choices[0].message.content')

pdf.section_title("4. Handling Tool Calls")
pdf.body_text(
    "handle_tool_calls iterates over all requested calls in one response "
    "(the model may ask for several at once), executes each, and returns tool-role messages:")
pdf.code_block(
    'def handle_tool_calls(message):\n'
    '    responses = []\n'
    '    for tool_call in message.tool_calls:\n'
    '        args = json.loads(tool_call.function.arguments)\n'
    '        if tool_call.function.name == "get_ticket_price":\n'
    '            result = get_ticket_price(args["destination_city"])\n'
    '        responses.append({\n'
    '            "role": "tool",\n'
    '            "content": str(result),\n'
    '            "tool_call_id": tool_call.id\n'
    '        })\n'
    '    return responses')

pdf.section_title("5. Tool Dispatch Registry Pattern")
pdf.body_text(
    "As the number of tools grows, a dispatch registry keeps the handler clean:")
pdf.code_block(
    'TOOL_HANDLERS = {\n'
    '    "get_ticket_price": lambda args: get_ticket_price(args["destination_city"]),\n'
    '    "set_ticket_price": lambda args: set_ticket_price(args["city"], float(args["price"])),\n'
    '}\n\n'
    'def handle_tool_calls(message):\n'
    '    responses = []\n'
    '    for tool_call in message.tool_calls:\n'
    '        handler = TOOL_HANDLERS.get(tool_call.function.name)\n'
    '        result  = handler(json.loads(tool_call.function.arguments))\n'
    '        responses.append({"role": "tool", "content": str(result),\n'
    '                           "tool_call_id": tool_call.id})\n'
    '    return responses')

pdf.section_title("6. Backing Tools with a Real Database (SQLite)")
pdf.body_text(
    "Tools are not limited to in-memory lookups \u2013 they can query real databases, "
    "call external APIs, or execute any Python code:")
pdf.code_block(
    'import sqlite3\n'
    'DB = "prices.db"\n\n'
    'def get_ticket_price(city):\n'
    '    with sqlite3.connect(DB) as conn:\n'
    '        cursor = conn.cursor()\n'
    '        cursor.execute("SELECT price FROM prices WHERE city = ?", (city.lower(),))\n'
    '        result = cursor.fetchone()\n'
    '    return f"Ticket to {city}: ${result[0]}" if result else "No price found"')

pdf.note_box(
    "Business implication: tool calling is what transforms a chatbot from a "
    "read-only question-answering system into an agent that can take actions \u2013 "
    "query databases, call booking APIs, update records, send emails, and more.")

# ════════════════════════════════════════════════════════════════════════════
# DAY 5
# ════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 5 \u2013 Multi-Modal AI Assistant",
                  "Image generation (DALL-E), TTS audio, gr.Blocks custom UI, agentic workflow")

pdf.section_title("1. Image Generation with DALL-E 3")
pdf.body_text(
    "OpenAI's images.generate endpoint produces images from text prompts. "
    "Requesting b64_json in response_format returns base64-encoded PNG data "
    "that can be decoded into a PIL Image for display in Gradio:")
pdf.code_block(
    'from PIL import Image\n'
    'from io import BytesIO\n'
    'import base64\n\n'
    'def artist(city):\n'
    '    resp = openai.images.generate(\n'
    '        model="dall-e-3",\n'
    '        prompt=f"A vibrant pop-art vacation image of {city}",\n'
    '        size="1024x1024",\n'
    '        n=1,\n'
    '        response_format="b64_json"\n'
    '    )\n'
    '    data = base64.b64decode(resp.data[0].b64_json)\n'
    '    return Image.open(BytesIO(data))')
pdf.note_box("Cost note: each DALL-E 3 image costs ~4 cents. Use sparingly during development.")

pdf.section_title("2. Text-to-Speech Audio")
pdf.body_text(
    "OpenAI's audio.speech.create endpoint converts text to spoken audio. "
    "The response is raw audio bytes that can be played directly in Gradio's gr.Audio component:")
pdf.code_block(
    'def talker(message):\n'
    '    response = openai.audio.speech.create(\n'
    '        model="gpt-4o-mini-tts",\n'
    '        voice="onyx",   # alternatives: alloy, coral\n'
    '        input=message\n'
    '    )\n'
    '    return response.content   # raw audio bytes')

pdf.section_title("3. Three Types of Gradio UI")
pdf.bullet("gr.Interface  \u2013 simple single-function UIs with automatic layout")
pdf.bullet("gr.ChatInterface \u2013 pre-built chat UI with history management")
pdf.bullet("gr.Blocks     \u2013 fully custom layout with explicit components and event wiring")
pdf.ln(2)
pdf.body_text("gr.Blocks is required when you need multiple output panels (e.g. chat + image + audio).")

pdf.section_title("4. gr.Blocks \u2013 Custom Multi-Panel Layout")
pdf.code_block(
    'with gr.Blocks() as ui:\n'
    '    with gr.Row():\n'
    '        chatbot      = gr.Chatbot(height=500, type="messages")\n'
    '        image_output = gr.Image(height=500, interactive=False)\n'
    '    with gr.Row():\n'
    '        audio_output = gr.Audio(autoplay=True)\n'
    '    with gr.Row():\n'
    '        message = gr.Textbox(label="Chat with our AI Assistant:")\n\n'
    '    # Chain events: submit text -> append to chatbot -> call chat()\n'
    '    message.submit(\n'
    '        put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]\n'
    '    ).then(\n'
    '        chat, inputs=chatbot, outputs=[chatbot, audio_output, image_output]\n'
    '    )\n\n'
    'ui.launch(inbrowser=True, auth=("ed", "bananas"))')

pdf.section_title("5. Event Chaining with .then()")
pdf.body_text(
    "In gr.Blocks, .then() chains callbacks sequentially. "
    "The first callback (put_message_in_chatbot) appends the user message, "
    "then the second callback (chat) runs the LLM + tools and returns all outputs at once.")

pdf.section_title("6. Full Multi-Modal Chat Function")
pdf.body_text(
    "The final chat() function integrates tool calling, text reply, TTS audio, "
    "and image generation into a single agentic workflow:")
pdf.code_block(
    'def chat(history):\n'
    '    messages = [{"role": "system", "content": system_message}] + history\n'
    '    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)\n'
    '    cities = []\n\n'
    '    while response.choices[0].finish_reason == "tool_calls":\n'
    '        tool_msg = response.choices[0].message\n'
    '        results, cities = handle_tool_calls_and_return_cities(tool_msg)\n'
    '        messages += [tool_msg] + results\n'
    '        response = openai.chat.completions.create(\n'
    '            model=MODEL, messages=messages, tools=tools)\n\n'
    '    reply = response.choices[0].message.content\n'
    '    history += [{"role": "assistant", "content": reply}]\n'
    '    voice = talker(reply)                          # TTS\n'
    '    image = artist(cities[0]) if cities else None  # DALL-E\n'
    '    return history, voice, image')

pdf.section_title("7. Agentic Workflow Summary")
pdf.note_box(
    "Day 5 represents the first fully agentic AI assistant: "
    "it reasons about the user's request, decides which tools to call, "
    "executes them (database lookup), synthesises a reply, converts it to audio, "
    "and generates a matching image \u2013 all autonomously in response to a single user message. "
    "This architecture is a direct precursor to the 7-agent pipeline built in Week 8.")

# ════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE TABLE
# ════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Quick Reference \u2013 Week 2 Concepts at a Glance")

rows = [
    ("Concept", "Day", "Key Takeaway"),
    ("Multi-provider via OpenAI client", "1", "Swap base_url + api_key; same API for all providers"),
    ("reasoning_effort parameter", "1", "Controls inference-time compute on reasoning models"),
    ("Native SDKs (google.genai, Anthropic)", "1", "Alternative to OpenAI client; provider-specific features"),
    ("OpenRouter", "1", "Single key/endpoint to access 100+ models"),
    ("LangChain", "1", "Heavyweight abstraction; ChatOpenAI wraps LLM calls"),
    ("LiteLLM", "1", "Lightweight universal completion(); exposes cost tracking"),
    ("Prompt caching", "1", "Cache static prefix to save 4-10x on repeated large prompts"),
    ("Adversarial chatbots", "1", "Swap assistant/user roles to orchestrate multi-model dialogue"),
    ("gr.Interface", "2", "Simple Gradio UI: fn + inputs + outputs"),
    ("share / auth / inbrowser", "2", "Gradio launch options for sharing and access control"),
    ("Streaming with yield", "2", "Generator callbacks enable token-by-token display"),
    ("Multi-model dropdown", "2", "gr.Dropdown lets users pick a model at runtime"),
    ("gr.ChatInterface", "3", "One-liner chatbot UI; passes (message, history) to callback"),
    ("Dynamic system prompt", "3", "Modify system message at runtime based on user input"),
    ("Tool calling (function calling)", "4", "LLM requests you run a function; result fed back in"),
    ("Tool schema (JSON)", "4", "Describes name, description, parameters of callable function"),
    ("Tool calling loop (while)", "4", "Repeat until finish_reason != 'tool_calls'"),
    ("Tool dispatch registry", "4", "Dict mapping tool names to handler lambdas"),
    ("SQLite-backed tools", "4", "Tools can query real databases, not just in-memory data"),
    ("DALL-E 3 image generation", "5", "openai.images.generate(); returns b64_json or URL"),
    ("Text-to-speech (TTS)", "5", "openai.audio.speech.create(); voice param selects voice"),
    ("gr.Blocks", "5", "Custom multi-panel layouts with explicit event wiring"),
    ("Event chaining (.then())", "5", "Chain sequential callbacks in gr.Blocks"),
    ("Full agentic assistant", "5", "Tools + TTS + image generation in one chat function"),
]

col_widths = [78, 12, 92]
line_h = 6.5

def draw_table_header(pdf, headers, col_widths):
    pdf.set_font("Arial", "B", 8.5)
    pdf.set_fill_color(20, 70, 150)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, border=1, fill=True)
    pdf.ln()

def draw_table_row(pdf, row, col_widths, fill, line_h=6.5):
    pdf.set_font("Arial", "", 8)
    color = (230, 238, 255) if fill else (255, 255, 255)
    pdf.set_fill_color(*color)
    pdf.set_text_color(0, 0, 0)

    # Measure how many lines the last column needs
    lines = pdf.multi_cell(col_widths[2], line_h, row[2],
                           border=0, fill=False, dry_run=True, output="LINES")
    row_h = max(1, len(lines)) * line_h

    x_start = pdf.l_margin
    y_start  = pdf.get_y()

    # Page break: re-draw header on new page
    if y_start + row_h > pdf.page_break_trigger:
        pdf.add_page()
        draw_table_header(pdf, rows[0], col_widths)
        y_start = pdf.get_y()

    # Col 0 & 1 – fixed height
    pdf.set_xy(x_start, y_start)
    pdf.cell(col_widths[0], row_h, row[0], border=1, fill=fill, align="L")
    pdf.cell(col_widths[1], row_h, row[1], border=1, fill=fill, align="C")

    # Col 2 – multi_cell (may wrap)
    pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)
    pdf.multi_cell(col_widths[2], line_h, row[2], border=1, fill=fill, align="L")

    # Advance cursor to start of next row
    pdf.set_xy(x_start, y_start + row_h)

draw_table_header(pdf, rows[0], col_widths)

for idx, row in enumerate(rows[1:]):
    draw_table_row(pdf, row, col_widths, fill=(idx % 2 == 0), line_h=line_h)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week2_summary.pdf")
pdf.output(out_path)
print(f"PDF saved to: {out_path}")
