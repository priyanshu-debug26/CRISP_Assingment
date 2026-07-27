# Prompt Engineering Mastery Workbench 🛠️

A professional terminal-based (CLI) workbench designed as an educational workshop project for Generative AI. The application executes 20 diverse prompting examples across four foundational prompt engineering techniques, prints beautiful formatted results in the console, and compiles a comprehensive Markdown evaluation report automatically.

Built using **Python 3**, **Groq API** (Llama 3 models), **python-dotenv**, and **Rich**.

---

## Project Overview

Prompt engineering is the core skill required to build reliable LLM applications. This workbench serves as a demonstration laboratory where students can evaluate, trace, and compare prompting outcomes. The tool supports running live connections to Groq or executing in offline Mock Mode, drawing from a high-fidelity database of realistic simulated outputs.

---

## Features

1. **Four Prompts Categories**:
   - **Zero-Shot Prompting**: Tests direct, context-free requests (programming, summarizing, translating, classifying, creative writing).
   - **Few-Shot Prompting**: Demonstrates format-matching via input-output pairs (sentiment analysis, active-passive voice, SQL formulation).
   - **Chain-of-Thought Prompting**: Forces step-by-step mathematical, logical, and decision-making traces.
   - **Role Prompting**: Applies domain expert personas (Software Engineer, Coach, FAANG Interviewer) to guide formatting and critiquing depth.
2. **Offline Mock Mode fallback**: Includes 20 pre-written, detailed, high-fidelity mock answers that match real LLM structures, allowing testing offline without API keys.
3. **Rich CLI Output**: Renders beautiful ASCII banners, execution mode stats, progress spinners, summary grids of execution statuses, and panels.
4. **Auto-Generated Report**: Compiles a clean `prompt_engineering_results.md` file after every run, detailing the prompts, results, and insights.

---

## Project Structure

```
assignment_1/
├── main.py                  # CLI controller and argument parser
├── api_helper.py            # Live Groq API client loader and Mock database engine
├── prompts.py               # Prompt definitions database (20 prompts)
├── markdown_generator.py    # Auto-compile markdown summaries helper
├── requirements.txt         # Package dependencies (groq, python-dotenv, rich)
├── README.md                # Project documentation and manual
├── reflection_report.md     # Workshop reflection template for students
├── .env.example             # Environment configuration template
└── .gitignore               # Excluded file paths list
```

---

## Technologies Used

- **Python 3**: Main runtime.
- **Groq SDK**: Primary client to execute llama-3.3 models.
- **Rich**: Terminal formatting (banners, tables, panels).
- **Python-dotenv**: Environment configuration.

---

## Installation

### 1. Set Up Project Directory
Navigate to the `Assignment 1` folder in your terminal:
```bash
cd "Assignment 1"
```

### 2. Virtual Environment Setup
Formulate a local environment to isolate dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Load Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

1. Copy the `.env.example` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure your credentials:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   GROQ_DEFAULT_MODEL=llama3-8b-8192
   ```

---

## Running the Project

The workbench supports three primary execution modes and custom model configurations.

### 1. Auto Mode
Checks if `GROQ_API_KEY` exists in your `.env` or system environment. If found, runs live; if absent, falls back to Mock Mode automatically:
```bash
python main.py
```

### 2. Force Live Mode
Forces execution through the live Groq API (will raise credentials warning if key is missing):
```bash
python main.py --live
```

### 3. Force Mock Mode
Forces execution using the offline mock response database:
```bash
python main.py --mock
```

### 4. Custom Model Configuration
Specify any valid Groq model identifier from the command line:
```bash
python main.py --live --model llama-3.3-70b-specdec
```

---

## Example Output

### Terminal CLI Preview
```text
 ╔══════════════════════════════════════════════════════════════════════╗
 ║                PROMPT ENGINEERING WORKSHOP WORKBENCH                 ║
 ╚══════════════════════════════════════════════════════════════════════╝
 Execution Mode: MOCK MODE | Model: llama3-8b-8192

 Running prompts trace...
 ⠋ Zero-Shot Programming completed.
 ...
 [Results Summary Grid]
 ┌──────────────────────┬──────────────────────────┬──────────────┐
 │ ID                   │ Category                 │ Status       │
 ├──────────────────────┼──────────────────────────┼──────────────┤
 │ zero_shot_program    │ Zero-Shot Prompting      │ ✅ Completed │
 └──────────────────────┴──────────────────────────┴──────────────┘
```

---

## Screenshots

<img width="1651" height="595" alt="image" src="https://github.com/user-attachments/assets/ca102108-09f4-4308-941c-235ce35cfcf7" />
<img width="953" height="691" alt="image" src="https://github.com/user-attachments/assets/ec447157-eee6-4f7b-871b-64de1ecf8f94" />
<img width="1637" height="904" alt="image" src="https://github.com/user-attachments/assets/a4d89909-9910-4a6c-bfd5-734f61038baf" />
<img width="1655" height="910" alt="image" src="https://github.com/user-attachments/assets/090e0440-037a-4f7e-8199-593b32611bd0" />

---

## Future Improvements

- Add token-consumption logging.
- Support side-by-side prompt comparisons across different models.
- Implement export formats (JSON, CSV).

---
