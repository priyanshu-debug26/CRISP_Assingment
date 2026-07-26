# Reflection Report: Assignment 1 - Prompt Engineering Mastery

## 1. Objective
The objective of this assignment is to explore and master four foundational prompt engineering techniques: Zero-Shot Prompting, Few-Shot Prompting, Chain-of-Thought (CoT) Prompting, and Role Prompting. By testing these methods across multiple domains (programming, math, logical deduction, creative writing, and system security) using the Groq API, we analyze how structuring input impacts model outputs, response layouts, and accuracy.

---

## 2. Techniques Learned

### Zero-Shot Prompting
Zero-shot prompting presents a query directly to the LLM without any prior examples. It depends entirely on the model's pre-trained knowledge base.
- *Use Case*: Direct calculations, summaries, languages translations, and code blocks creation.
- *Key Learny*: The model must be given precise context parameters (e.g., 'Translate to French and use formal vocabulary') to guide tone.

### Few-Shot Prompting
Few-shot prompting feeds the model multiple example demonstrations of (Input -> Output) pairs before presenting the target task.
- *Use Case*: Semantic code labeling, syntax styling, emojis parsing, and database SQL syntax matching.
- *Key Learny*: Demonstrations establish structural boundaries, prompting the model to match style constraints.

### Chain-of-Thought (CoT) Prompting
Chain-of-Thought prompting directs the LLM to write out its logical reasoning, calculations, or steps before concluding with the final answer.
- *Use Case*: Complex algebraic calculations, reasoning grids, scheduling problems, and algorithm walkthroughs.
- *Key Learny*: Forcing the model to write out intermediate steps prevents the model from generating calculations off the top of its head, reducing logical errors.

### Role Prompting
Role prompting assigns a specific persona, background, or job title (e.g. Cybersecurity Expert, Historian) to the model before asking a question.
- *Use Case*: In-depth design reviews, structured code reviews, executive reports, and academic text composition.
- *Key Learny*: Personas shape both vocabulary style (academic vs executive) and depth of critique (focusing on system architecture vs simple syntax).

---

## 3. Comparison Between Prompt Types

| Prompting Technique | Input Complexity | output Quality & Control | Best For | Potential Drawbacks |
|---|---|---|---|---|
| **Zero-Shot** | Low | Moderate | Standard facts, simple tasks | Vulnerable to formatting deviations |
| **Few-Shot** | Medium | High (matches templates) | Custom patterns, classifications | Larger token consumption |
| **Chain-of-Thought** | High | High (logical correctness) | Calculations, reasoning | Longer execution times |
| **Role Prompting** | Medium | High (styled response) | Domain-specific critiques | Persona override risks |

---

## 4. Challenges & Mitigations
- **Structured JSON and Regex Stripping**: Prompting models to return JSON can sometimes output markdown decorators which break string parsers.
  - *Mitigation*: Sanitizing strings using regular expression filters before parsing.
- **API Failures and Rate Limits**: Running multiple consecutive calls can trigger rate limits on Groq.
  - *Mitigation*: Incorporating client delay spacing (`time.sleep`) and designing a realistic fallback Mock database.

---

## 5. Learning Outcomes
- Developed modular Python architectures separating prompt databases, client utilities, report engines, and CLI outputs.
- Acquired hands-on experience using the `Rich` terminal library to render banners, summary status grids, progress status spinners, and diagnostic logs.
- Mastered methods to structure instructions, format context samples, enforce mathematical logic, and adjust model temperature.

---

## 6. Student Notes & Workshop Observations
*Student: Use the sections below to document your personal findings during execution.*

### Personal Observations
`[STUDENT TODO: Write your custom observations about how model outputs differed between forced Live mode and Mock mode here. Did some prompts trigger faster than others?]`

### Performance Critiques
`[STUDENT TODO: Review the generated prompt_engineering_results.md file. Did the model fail to satisfy any constraint in Zero-Shot? Did the Few-Shot emojis look correctly matching?]`

### Future Improvements
`[STUDENT TODO: What features would you add to this workbench? Examples: adding token usage charts, comparing responses across multiple Groq models side-by-side, or exporting responses into CSV format.]`
