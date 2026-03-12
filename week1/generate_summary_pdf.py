from fpdf import FPDF
import os

FONT_DIR = "C:/Windows/Fonts"

class SummaryPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Add Unicode-capable Arial font
        self.add_font("Arial", "", f"{FONT_DIR}/arial.ttf")
        self.add_font("Arial", "B", f"{FONT_DIR}/arialbd.ttf")
        self.add_font("Arial", "I", f"{FONT_DIR}/ariali.ttf")
        self.add_font("Arial", "BI", f"{FONT_DIR}/arialbi.ttf")
        self.add_font("Courier", "", f"{FONT_DIR}/cour.ttf")
        self.add_font("Courier", "B", f"{FONT_DIR}/courbd.ttf")

    def header(self):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(30, 30, 60)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "LLM Engineering \u2013 Week 1 Key Concepts", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title, subtitle=""):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(60, 90, 160)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        if subtitle:
            self.set_font("Arial", "I", 10)
            self.set_fill_color(220, 225, 245)
            self.set_text_color(50, 50, 80)
            self.cell(0, 7, subtitle, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.set_text_color(30, 60, 140)
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
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(180, 180, 180)
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

# ─── COVER / INTRO ────────────────────────────────────────────────────────────
pdf.set_font("Arial", "B", 20)
pdf.set_text_color(30, 30, 60)
pdf.ln(6)
pdf.cell(0, 12, "LLM Engineering \u2013 Week 1", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Arial", "B", 15)
pdf.set_text_color(60, 90, 160)
pdf.cell(0, 9, "Key Concepts Summary: Day 1, 2, 4 & 5", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_text_color(0, 0, 0)
pdf.ln(5)
pdf.set_font("Arial", "", 10)
pdf.set_fill_color(235, 240, 255)
pdf.multi_cell(0, 6,
    "This document summarises the most important concepts, techniques and code patterns "
    "introduced during Week 1 of the LLM Engineering course (Days 1, 2, 4 and 5). "
    "It is designed as a quick-reference companion alongside the course notebooks.",
    fill=True)
pdf.ln(8)

# ══════════════════════════════════════════════════════════════════════════════
# DAY 1
# ══════════════════════════════════════════════════════════════════════════════
pdf.chapter_title("Day 1 \u2013 Your First Frontier LLM Project",
                  "Web Summariser using the OpenAI Chat Completions API")

pdf.section_title("1. Project Goal")
pdf.body_text(
    "Build a 'Reader's Digest' web browser: give it a URL and receive an AI-generated "
    "summary of the page contents. This introduces the full workflow of calling a "
    "Frontier model (GPT-4.1-mini) with custom prompts.")

pdf.section_title("2. Core Concept \u2013 System & User Prompts")
pdf.body_text(
    "Every request to an OpenAI-compatible model is structured as a list of messages "
    "with roles. Two roles dominate Day 1:")
pdf.bullet("system \u2013 instructs the model on its persona and the task")
pdf.bullet("user   \u2013 provides the specific input for this call")
pdf.ln(2)
pdf.code_block(
    'messages = [\n'
    '    {"role": "system", "content": "You are a snarky summariser..."},\n'
    '    {"role": "user",   "content": "Here are the contents of a website: ..."}\n'
    ']')

pdf.section_title("3. OpenAI Python Client \u2013 Making the Call")
pdf.body_text(
    "The openai package is a thin Python wrapper around the HTTP endpoint "
    "https://api.openai.com/v1/chat/completions. "
    "The response object contains the model's reply at choices[0].message.content.")
pdf.code_block(
    'from openai import OpenAI\n'
    'openai = OpenAI()   # reads OPENAI_API_KEY from environment\n\n'
    'response = openai.chat.completions.create(\n'
    '    model="gpt-4.1-mini",\n'
    '    messages=messages\n'
    ')\n'
    'result = response.choices[0].message.content')

pdf.section_title("4. Web Scraping Helper")
pdf.body_text(
    "fetch_website_contents(url) retrieves the plain text of a webpage for injection "
    "into the user prompt. JavaScript-heavy sites (React apps) require Selenium / Playwright "
    "because static HTTP fetching returns an empty page.")

pdf.section_title("5. Business Use Case \u2013 Summarisation")
pdf.note_box(
    "Summarisation is one of the most universal Gen-AI applications: news digests, "
    "financial reports, resume screening, email subject-line generation, and more. "
    "The Day 1 exercise includes a self-practice task: auto-generating a subject line "
    "for an email body.")

# ══════════════════════════════════════════════════════════════════════════════
# DAY 2
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 2 \u2013 The Chat Completions API & Model Ecosystem",
                  "OpenAI-Compatible Endpoints, Google Gemini, and Local Ollama")

pdf.section_title("1. What Is the Chat Completions API?")
pdf.body_text(
    "The Chat Completions API was invented by OpenAI and is now the de-facto industry "
    "standard. It is called 'Chat Completions' because the model is asked: "
    "'given this conversation, predict what should come next'. "
    "Every other provider has since adopted the same interface.")

pdf.section_title("2. Under the Hood \u2013 Raw HTTP")
pdf.body_text(
    "The openai Python package is just a convenience wrapper. The same call can be "
    "made directly with requests:")
pdf.code_block(
    'import requests\n'
    'headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}\n'
    'payload = {\n'
    '    "model": "gpt-5-nano",\n'
    '    "messages": [{"role": "user", "content": "Tell me a fun fact"}]\n'
    '}\n'
    'response = requests.post(\n'
    '    "https://api.openai.com/v1/chat/completions",\n'
    '    headers=headers, json=payload\n'
    ')\n'
    'result = response.json()["choices"][0]["message"]["content"]')

pdf.section_title("3. OpenAI-Compatible Endpoints")
pdf.body_text(
    "Because OpenAI's API became ubiquitous, every major provider now exposes an "
    "identical endpoint. You simply swap base_url and api_key:")
pdf.bullet("Google Gemini  \u2192  base_url = 'https://generativelanguage.googleapis.com/v1beta/openai/'")
pdf.bullet("Ollama (local) \u2192  base_url = 'http://localhost:11434/v1',  api_key='ollama'")
pdf.ln(2)
pdf.code_block(
    'gemini = OpenAI(\n'
    '    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",\n'
    '    api_key=os.getenv("GOOGLE_API_KEY")\n'
    ')\n'
    'gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=[...])')

pdf.section_title("4. Running Models Locally with Ollama")
pdf.body_text(
    "Ollama lets you run open-source models (LLaMA 3.2, DeepSeek-R1, etc.) "
    "entirely on your machine\u2014no API charges and no data leaving your box.")
pdf.bullet("Install from https://ollama.com, then run: ollama serve")
pdf.bullet("Pull a model: ollama pull llama3.2")
pdf.bullet("Smaller option for low-RAM machines: llama3.2:1b")
pdf.bullet("DeepSeek 1.5B (reasoning model, distilled): deepseek-r1:1.5b")
pdf.ln(2)
pdf.code_block(
    'ollama = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")\n'
    'response = ollama.chat.completions.create(\n'
    '    model="llama3.2", messages=[{"role": "user", "content": "Tell me a fun fact"}]\n'
    ')')

pdf.section_title("5. Homework")
pdf.note_box(
    "Upgrade the Day 1 web summariser to use a local Ollama model instead of OpenAI. "
    "Trade-off: free & private, but noticeably less capable than a frontier model.")

# ══════════════════════════════════════════════════════════════════════════════
# DAY 4
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 4 \u2013 Tokenisation & The Illusion of LLM Memory",
                  "tiktoken, stateless inference, and the conversation-replay trick")

pdf.section_title("1. Tokenisation")
pdf.body_text(
    "LLMs do not process characters or words\u2014they process tokens. "
    "A token is a frequently-occurring sub-word fragment. "
    "The tiktoken library (used by OpenAI) lets you inspect this directly.")
pdf.code_block(
    'import tiktoken\n'
    'encoding = tiktoken.encoding_for_model("gpt-4.1-mini")\n'
    'tokens = encoding.encode("Hi my name is Ed and I like banoffee pie")\n'
    '# -> [12194, 922, 1308, 382, 6117, 326, 357, 1299, 9171, 26458, 5148]\n\n'
    'for token_id in tokens:\n'
    '    print(token_id, "=", encoding.decode([token_id]))\n'
    '# "banoffee" splits into two tokens: ban (9171) + offee (26458)')

pdf.body_text("Key observations:")
pdf.bullet("Common English words are usually a single token.")
pdf.bullet("Rare words, technical jargon, or non-English text may split across many tokens.")
pdf.bullet("Spaces are often baked into the token that follows them (e.g. ' and' = one token).")
pdf.bullet("Token limits (context windows) are measured in tokens, not words.")

pdf.section_title("2. LLMs Are Stateless")
pdf.body_text(
    "Every single call to an LLM API is completely independent. "
    "The model has no memory of previous calls whatsoever.")
pdf.code_block(
    '# Call 1 - the model greets Ed\n'
    'messages = [\n'
    '    {"role": "system",    "content": "You are a helpful assistant"},\n'
    '    {"role": "user",      "content": "Hi! I\'m Ed!"}\n'
    ']\n'
    '# response -> "Hello, Ed!"\n\n'
    '# Call 2 - completely new call, Ed is forgotten\n'
    'messages = [\n'
    '    {"role": "system",    "content": "You are a helpful assistant"},\n'
    '    {"role": "user",      "content": "What\'s my name?"}\n'
    ']\n'
    '# response -> "I\'m sorry, I don\'t know your name."')

pdf.section_title("3. Simulating Memory \u2013 The Conversation-Replay Trick")
pdf.body_text(
    "To give the impression of memory, AI engineers replay the entire conversation "
    "history on every call by adding previous turns as assistant messages:")
pdf.code_block(
    'messages = [\n'
    '    {"role": "system",    "content": "You are a helpful assistant"},\n'
    '    {"role": "user",      "content": "Hi! I\'m Ed!"},\n'
    '    {"role": "assistant", "content": "Hi Ed! How can I assist you today?"},\n'
    '    {"role": "user",      "content": "What\'s my name?"}\n'
    ']\n'
    '# response -> "Your name is Ed!"')

pdf.body_text("Five principles to internalise:")
pdf.bullet("1. Every call is stateless \u2013 a blank slate.")
pdf.bullet("2. The entire conversation is sent as input on every call.")
pdf.bullet("3. The 'memory' is an illusion created by replaying history.")
pdf.bullet("4. ChatGPT and every chat product use exactly this trick.")
pdf.bullet("5. Longer conversations cost more because more tokens are sent each time.")

pdf.note_box(
    "Cost implication: including the full conversation history means you pay for every "
    "prior turn on every subsequent call. This is intentional \u2013 it gives the model the "
    "context it needs to produce coherent replies.")

# ══════════════════════════════════════════════════════════════════════════════
# DAY 5
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Day 5 \u2013 Full Business Solution: Company Brochure Generator",
                  "Multi-call LLM pipelines, JSON mode, streaming, and agentic patterns")

pdf.section_title("1. Business Challenge")
pdf.body_text(
    "Extend the Day 1 summariser into a production-quality tool that automatically "
    "generates a marketing brochure for any company given only its website URL. "
    "The brochure is aimed at prospective customers, investors, and recruits.")

pdf.section_title("2. Pipeline Architecture (Early Agentic Pattern)")
pdf.body_text(
    "Day 5 introduces the first multi-step LLM pipeline \u2013 a precursor to full Agentic AI:")
pdf.bullet("Step 1: Scrape the landing page and collect all hyperlinks.")
pdf.bullet("Step 2: Ask GPT to classify which links are relevant (About, Careers, Products...).")
pdf.bullet("Step 3: Scrape each relevant page.")
pdf.bullet("Step 4: Assemble all scraped content and ask GPT to write the brochure.")
pdf.ln(2)
pdf.body_text("This is an example of the Orchestrator-Worker agentic design pattern "
              "where one LLM call decides what to do, and subsequent calls carry out the work.")

pdf.section_title("3. Structured JSON Output (JSON Mode)")
pdf.body_text(
    "To reliably parse the model's response in Step 2, we use response_format='json_object'. "
    "This forces the model to return well-formed JSON that can be parsed with json.loads().")
pdf.code_block(
    'response = openai.chat.completions.create(\n'
    '    model=MODEL,\n'
    '    messages=[\n'
    '        {"role": "system", "content": link_system_prompt},\n'
    '        {"role": "user",   "content": get_links_user_prompt(url)}\n'
    '    ],\n'
    '    response_format={"type": "json_object"}\n'
    ')\n'
    'links = json.loads(response.choices[0].message.content)')

pdf.section_title("4. One-Shot Prompting")
pdf.body_text(
    "The link-classification prompt includes a worked example of the expected JSON structure "
    "(one-shot prompting). This greatly improves output reliability without fine-tuning:")
pdf.code_block(
    'link_system_prompt = """\n'
    'You are provided with a list of links found on a webpage...\n'
    'Respond in JSON as in this example:\n'
    '{\n'
    '  "links": [\n'
    '    {"type": "about page", "url": "https://full.url/goes/here/about"},\n'
    '    {"type": "careers page", "url": "https://another.url/careers"}\n'
    '  ]\n'
    '}\n'
    '"""')

pdf.section_title("5. Prompt Tone Control")
pdf.body_text(
    "A single word change in the system prompt dramatically shifts the output style. "
    "This illustrates how easy it is to adjust the 'personality' of generated content:")
pdf.bullet("Professional: 'You are an assistant that analyzes company pages and creates a short brochure...'")
pdf.bullet("Humorous: '...creates a short, humorous, entertaining, witty brochure...'")

pdf.section_title("6. Streaming Responses")
pdf.body_text(
    "Instead of waiting for the full response, we can stream tokens as they are produced "
    "for a typewriter-style UX. The key parameter is stream=True:")
pdf.code_block(
    'stream = openai.chat.completions.create(\n'
    '    model="gpt-4.1-mini",\n'
    '    messages=[...],\n'
    '    stream=True\n'
    ')\n\n'
    'response = ""\n'
    'display_handle = display(Markdown(""), display_id=True)\n'
    'for chunk in stream:\n'
    '    response += chunk.choices[0].delta.content or ""\n'
    '    update_display(Markdown(response), display_id=display_handle.display_id)')

pdf.section_title("7. Business Applications of Content Generation")
pdf.note_box(
    "Content generation is one of the highest-value Gen-AI use cases: marketing brochures, "
    "product tutorials from specs, personalised email campaigns, job descriptions, "
    "investor summaries, and more. Day 5 marks the first step toward fully autonomous "
    "Agentic AI, a topic that returns in Week 8 with a 7-agent pipeline.")

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE TABLE
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("Quick Reference \u2013 Week 1 Concepts at a Glance")

data = [
    ("Concept", "Day", "Key Takeaway"),
    ("Chat Completions API", "1 & 2", "Industry-standard interface; list of role/content dicts"),
    ("System vs User prompt", "1", "System sets persona/task; User provides the input"),
    ("openai Python library", "1 & 2", "Thin HTTP wrapper \u2013 no model code inside"),
    ("OpenAI-Compatible Endpoints", "2", "All major providers expose the same API shape"),
    ("Google Gemini via OpenAI SDK", "2", "Swap base_url + api_key; model name changes"),
    ("Ollama (local models)", "2", "Free, private, lower quality; base_url=localhost:11434"),
    ("Tokenisation", "4", "LLMs process sub-word tokens; use tiktoken to inspect"),
    ("LLM Statelessness", "4", "Every call starts fresh \u2013 no built-in memory"),
    ("Conversation Replay", "4", "Replay full history as messages to simulate memory"),
    ("JSON Mode", "5", "response_format={'type':'json_object'} for parseable output"),
    ("One-Shot Prompting", "5", "Include one example in the prompt to guide format/style"),
    ("Streaming", "5", "stream=True yields tokens incrementally for live display"),
    ("Agentic Pipeline", "5", "Chain multiple LLM calls: planner \u2192 executor \u2192 writer"),
]

col_widths = [72, 18, 92]
pdf.set_font("Arial", "B", 9)
pdf.set_fill_color(40, 70, 150)
pdf.set_text_color(255, 255, 255)
for i, header in enumerate(data[0]):
    pdf.cell(col_widths[i], 7, header, border=1, fill=True)
pdf.ln()

pdf.set_font("Arial", "", 8.5)
for row_idx, row in enumerate(data[1:]):
    fill = row_idx % 2 == 0
    if fill:
        pdf.set_fill_color(235, 240, 255)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    y_before = pdf.get_y()
    x_before = pdf.get_x()
    # Render first two cols as fixed cells, last as multi_cell
    pdf.cell(col_widths[0], 7, row[0], border=1, fill=fill)
    pdf.cell(col_widths[1], 7, row[1], border=1, fill=fill)
    pdf.multi_cell(col_widths[2], 7, row[2], border=1, fill=fill)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week1_summary.pdf")
pdf.output(out_path)
print(f"PDF saved to: {out_path}")
