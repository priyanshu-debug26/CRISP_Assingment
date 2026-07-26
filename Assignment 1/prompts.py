# Prompt Engineering Examples Database
# Contains 20 unique prompts across 4 techniques

PROMPTS = [
    # ==========================================
    # CATEGORY 1: ZERO-SHOT PROMPTING
    # ==========================================
    {
        "id": "zero_shot_programming",
        "category": "Zero-Shot Prompting",
        "domain": "Programming",
        "description": "Generate a Python function to compute the nth Fibonacci number.",
        "prompt": "Write a Python function called `nth_fibonacci(n)` that returns the nth Fibonacci number. Implement it using dynamic programming to ensure O(n) time complexity. Include brief docstrings and comments. Do not explain the concept of Fibonacci, just return the code.",
        "observation": "Zero-shot prompting works well for standard programming tasks since modern LLMs have extensive pre-training on code syntax and algorithms, requiring no context demonstrations."
    },
    {
        "id": "zero_shot_summarization",
        "category": "Zero-Shot Prompting",
        "domain": "Summarization",
        "description": "Summarize the core concept of Quantum Computing.",
        "prompt": "Summarize the core working principles of Quantum Computing in exactly three bullet points. Focus on superposition, entanglement, and qubits. Keep the vocabulary accessible to a high school student.",
        "observation": "For summarization, zero-shot prompting relies on the model's internal knowledge base to extract and condense key principles based on constraint instructions (e.g., three bullet points, high school level)."
    },
    {
        "id": "zero_shot_translation",
        "category": "Zero-Shot Prompting",
        "domain": "Translation",
        "description": "Translate a formal business letter segment to French.",
        "prompt": "Translate the following English business correspondence paragraph into formal French suitable for executive communications:\n'We appreciate your partnership and are excited to review the upcoming project deliverables next week. Please let us know if your team requires any additional technical documentation.'",
        "observation": "Zero-shot translation leverages multilingual pre-training. Specifying the target style ('formal French for executive communications') guides the tone without needing few-shot examples."
    },
    {
        "id": "zero_shot_classification",
        "category": "Zero-Shot Prompting",
        "domain": "Classification",
        "description": "Classify a product review's sentiment.",
        "prompt": "Analyze the sentiment of the following product review and classify it as POSITIVE, NEGATIVE, or NEUTRAL. Return ONLY the classification word. No other text.\nReview: 'The device works reasonably well once set up, but the user manual was incredibly confusing and it took me two hours to get it connected to my Wi-Fi.'",
        "observation": "Zero-shot classification relies on the LLM's semantic understanding of descriptive words. Adding constraints like 'Return ONLY the classification word' ensures clean programmatic extraction."
    },
    {
        "id": "zero_shot_writing",
        "category": "Zero-Shot Prompting",
        "domain": "Creative Writing",
        "description": "Write a sci-fi story opening.",
        "prompt": "Write a compelling two-sentence opening of a science fiction novel where humanity has discovered that the universe is actually a digital simulation, and the simulator is about to reboot.",
        "observation": "Zero-shot creative writing utilizes the LLM's ability to combine disparate narrative concepts (simulations, reboots, human discovery) into a cohesive literary hook."
    },

    # ==========================================
    # CATEGORY 2: FEW-SHOT PROMPTING
    # ==========================================
    {
        "id": "few_shot_sentiment",
        "category": "Few-Shot Prompting",
        "domain": "Sentiment Analysis",
        "description": "Classify detailed feedback using few-shot examples.",
        "prompt": "Classify customer feedback into one of three classes: [Bug Report, Feature Request, Customer Support].\n\n"
                  "Example 1:\n"
                  "Feedback: The application crashes immediately when I tap the upload button.\n"
                  "Class: Bug Report\n\n"
                  "Example 2:\n"
                  "Feedback: It would be awesome if we could export the reports directly into Google Sheets format.\n"
                  "Class: Feature Request\n\n"
                  "Example 3:\n"
                  "Feedback: I forgot my password and my security question answers, can you help me recover my profile?\n"
                  "Class: Customer Support\n\n"
                  "Input:\n"
                  "Feedback: I noticed that the search bar ignores capitalization, which makes it hard to find specific product SKU codes.\n"
                  "Class:",
        "observation": "Few-shot prompting provides format and semantic context. By demonstrating input-output pairs, the model learns the classification boundaries and mimics the exact output style."
    },
    {
        "id": "few_shot_grammar",
        "category": "Few-Shot Prompting",
        "domain": "Active to Passive Voice",
        "description": "Transform sentence voices with structure examples.",
        "prompt": "Convert the active voice sentences into passive voice.\n\n"
                  "Active: The chef prepared a gourmet meal for the guests.\n"
                  "Passive: A gourmet meal was prepared for the guests by the chef.\n\n"
                  "Active: The dog chased the red ball across the field.\n"
                  "Passive: The red ball was chased across the field by the dog.\n\n"
                  "Active: The engineering team will deploy the update tonight.\n"
                  "Passive: The update will be deployed tonight by the engineering team.\n\n"
                  "Active: The committee approved the annual budget allocation.\n"
                  "Passive:",
        "observation": "This few-shot prompt establishes a clear grammatical transformation pattern, showing the model how to restructure parts of speech systematically."
    },
    {
        "id": "few_shot_categorization",
        "category": "Few-Shot Prompting",
        "domain": "Topic Categorization",
        "description": "Map news topics to categories using patterns.",
        "prompt": "Given a news headline, categorize it into [World News, Tech, Finance, Sports].\n\n"
                  "Headline: Apple announces new M-series chips for upcoming MacBook Pros.\n"
                  "Category: Tech\n\n"
                  "Headline: Inflation rates dip as central banks adjust interest rates.\n"
                  "Category: Finance\n\n"
                  "Headline: Real Madrid clinches UEFA Champions League title after final victory.\n"
                  "Category: Sports\n\n"
                  "Headline: Global leaders gather at United Nations assembly to discuss climate pacts.\n"
                  "Category: World News\n\n"
                  "Headline: Nasdaq composite slides as treasury yields tick upwards.\n"
                  "Category:",
        "observation": "Providing a balanced list of examples representing each target category guides the LLM on how to resolve ambiguous terms (like news headers containing tech/finance overlap)."
    },
    {
        "id": "few_shot_emojifier",
        "category": "Few-Shot Prompting",
        "domain": "Text-to-Emoji Translation",
        "description": "Translate literal descriptions to emoji strings.",
        "prompt": "Translate the following sentences into a sequence of 3 relevant emojis.\n\n"
                  "Input: I bought some fresh coffee and read a book in the garden.\n"
                  "Output: ☕📖🏡\n\n"
                  "Input: We went to the beach and played soccer under the sun.\n"
                  "Output: 🏖️⚽☀️\n\n"
                  "Input: The rocket launched into space to study the stars and planets.\n"
                  "Output: 🚀🌌🪐\n\n"
                  "Input: It was raining heavily, so I stayed home and watched a scary movie.\n"
                  "Output:",
        "observation": "Few-shot examples are critical here because 'Translate to emoji sequence' is highly subjective. The examples anchor the length (3 emojis) and the literal matching style."
    },
    {
        "id": "few_shot_sql",
        "category": "Few-Shot Prompting",
        "domain": "SQL Query Generation",
        "description": "Generate SQL statements from English descriptions.",
        "prompt": "Translate natural language questions into PostgreSQL queries.\n\n"
                  "Table: employees (id, name, department_id, salary, hire_date)\n\n"
                  "Question: Find all employees who earn more than 80,000 USD.\n"
                  "Query: SELECT * FROM employees WHERE salary > 80000;\n\n"
                  "Question: Show the total salary budget for the Sales department.\n"
                  "Query: SELECT SUM(salary) FROM employees WHERE department_id = 'Sales';\n\n"
                  "Question: List the names of the 5 most recently hired employees.\n"
                  "Query: SELECT name FROM employees ORDER BY hire_date DESC LIMIT 5;\n\n"
                  "Question: Get the average salary of employees grouped by department_id.\n"
                  "Query:",
        "observation": "Few-shot prompts for database queries show the model the target SQL dialect (PostgreSQL) and the correct syntax styles matching table schema metadata."
    },

    # ==========================================
    # CATEGORY 3: CHAIN-OF-THOUGHT PROMPTING
    # ==========================================
    {
        "id": "cot_math",
        "category": "Chain-of-Thought Prompting",
        "domain": "Mathematics",
        "description": "Solve a multi-step math word problem with explanation.",
        "prompt": "Solve the following math word problem step-by-step. Explain your reasoning for each step before writing the final answer.\n\n"
                  "Problem: A school cafeteria ordered 12 crates of apples. Each crate contains 15 bags, and each bag contains 8 apples. "
                  "The kitchen staff used 3 full crates of apples on Monday. On Tuesday, they opened 2 more crates and used half of the apples in those crates. "
                  "How many apples are left in total?",
        "observation": "Chain-of-thought prompting forces the model to decompose numerical operations. By writing intermediate states, the model avoids mental math reasoning arithmetic errors."
    },
    {
        "id": "cot_logic",
        "category": "Chain-of-Thought Prompting",
        "domain": "Logical Reasoning",
        "description": "Solve a deductive puzzle step-by-step.",
        "prompt": "Solve this logic puzzle step-by-step. Work through the clues systematically to determine the final ordering:\n\n"
                  "Puzzle: Four runners (Alice, Bob, Charlie, and Diana) finished a race. "
                  "Clue 1: Alice finished after Bob but before Charlie.\n"
                  "Clue 2: Bob was not the winner.\n"
                  "Clue 3: Diana finished before Bob.\n\n"
                  "What was the exact finish order of all four runners from 1st to 4th place? Show your step-by-step logic.",
        "observation": "Deductive logic requires building a constraints list. Chain-of-thought prompts prompt the model to list candidates and eliminate options sequentially, mimicking human analytical workflows."
    },
    {
        "id": "cot_multistep",
        "category": "Chain-of-Thought Prompting",
        "domain": "Multi-step Planning",
        "description": "Solve a schedule optimization problem.",
        "prompt": "Solve this scheduling problem step-by-step:\n\n"
                  "Scenario: An office manager has to coordinate three meetings tomorrow.\n"
                  "- Meeting A is 1 hour long and must start after 9:00 AM.\n"
                  "- Meeting B is 2 hours long and cannot overlap with Meeting A.\n"
                  "- Meeting C is 1.5 hours long and must start exactly when Meeting B ends.\n"
                  "- The manager cannot attend meetings after 2:00 PM.\n"
                  "- Meeting A must happen before Meeting B.\n\n"
                  "Propose a valid schedule for meetings A, B, and C. Walk through the time constraints step-by-step to show how you arrived at the schedule.",
        "observation": "Multi-step schedule planning requires coordinating multiple timeline dependencies. CoT lets the model map out schedules, verify boundaries, and reformulate times if boundaries overlap."
    },
    {
        "id": "cot_algorithm",
        "category": "Chain-of-Thought Prompting",
        "domain": "Simple Algorithms",
        "description": "Trace the steps of a sorting algorithm manually.",
        "prompt": "Trace the execution of the Bubble Sort algorithm step-by-step on the following list of numbers: [4, 2, 7, 1].\n"
                  "Show the state of the list after each full pass (outer loop iteration) and explain the swaps made during that pass until the list is fully sorted.",
        "observation": "Tracing algorithms requires keeping track of index states. Chain-of-thought prevents code-execution hallucinations by making the model write out each iteration state clearly."
    },
    {
        "id": "cot_decision",
        "category": "Chain-of-Thought Prompting",
        "domain": "Decision Making",
        "description": "Analyze buy vs lease options with logic.",
        "prompt": "Help a small business owner make a decision step-by-step:\n\n"
                  "Scenario: The business needs a delivery van for 3 years.\n"
                  "- Option 1: Buy the van for 30,000 USD cash. After 3 years, sell it for 12,000 USD.\n"
                  "- Option 2: Lease the van for 350 USD per month. There is a non-refundable down payment of 2,000 USD.\n\n"
                  "Calculate the total cost of each option over the 3-year period step-by-step. Compare the financial cost, list at least two qualitative advantages of each option, and recommend the best choice based on your calculations.",
        "observation": "Complex decision-making prompts require both quantitative calculations and qualitative balances. CoT ensures the financial calculations are done first, providing a solid foundation for the recommendation."
    },

    # ==========================================
    # CATEGORY 4: ROLE PROMPTING
    # ==========================================
    {
        "id": "role_engineer",
        "category": "Role Prompting",
        "domain": "Senior Software Engineer",
        "description": "Review code from the perspective of an expert developer.",
        "prompt": "Act as a Senior Software Engineer with 15 years of experience in system design and clean code. "
                  "Review the following JavaScript code snippet. Critique it for security flaws, efficiency, and readability. "
                  "Suggest a refactored version of the code utilizing modern JavaScript best practices:\n\n"
                  "```javascript\n"
                  "function loginUser(username, password) {\n"
                  "    var sql = \"SELECT * FROM users WHERE user = '\" + username + \"' AND pass = '\" + password + \"'\";\n"
                  "    db.execute(sql);\n"
                  "    console.log(\"User logged in: \" + username);\n"
                  "}\n"
                  "```",
        "observation": "Role prompting influences both the tone and depth. By adopting a 'Senior Software Engineer' persona, the model focuses on clean architecture, security patterns (like SQL injection prevention), and professional code conventions."
    },
    {
        "id": "role_coach",
        "category": "Role Prompting",
        "domain": "Career Coach",
        "description": "Provide professional transition guidance.",
        "prompt": "Act as an executive Career Coach specializing in the technology sector. "
                  "Provide a structured, encouraging 3-step action plan for a Mid-level Frontend Developer who has 4 years of experience and wants to transition into an Engineering Manager role. "
                  "Focus on leadership skills, project ownership, and mentorship. Use a professional, supportive tone.",
        "observation": "Applying a 'Career Coach' persona changes the vocabulary to be mentoring, positive, and structured around actionable milestone career goals rather than dry facts."
    },
    {
        "id": "role_interviewer",
        "category": "Role Prompting",
        "domain": "Technical Interviewer",
        "description": "Design an interview question and assessment rubric.",
        "prompt": "Act as a Technical Interviewer for a Lead DevOps position at a FAANG company. "
                  "Formulate one challenging interview question regarding CI/CD pipeline automation and blue-green deployments. "
                  "Then, list the criteria for what constitutes a 'Junior', 'Mid', and 'Senior' level answer to this question.",
        "observation": "The 'Technical Interviewer' persona guides the model to construct assessment metrics (rubrics) rather than just giving answers, formatting them as a structured grading grid."
    },
    {
        "id": "role_historian",
        "category": "Role Prompting",
        "domain": "Historian",
        "description": "Analyze history with context and deep analysis.",
        "prompt": "Act as an academic Historian specializing in the European Renaissance. "
                  "Explain how the invention of the Gutenberg printing press in the 15th century transformed the distribution of educational and religious knowledge. "
                  "Incorporate historical context regarding literacy rates and the role of monastic scribes prior to the press. Maintain a scholarly, analytical tone.",
        "observation": "The 'Historian' persona guides the model to adopt a narrative, academic writing style, referencing societal shifts, historical background, and comparative conditions."
    },
    {
        "id": "role_security",
        "category": "Role Prompting",
        "domain": "Cybersecurity Expert",
        "description": "Explain security risks and mitigations.",
        "prompt": "Act as a Cybersecurity Expert (CISSP). "
                  "Explain the mechanism of a SQL Injection (SQLi) attack to a non-technical business executive. "
                  "Use an analogy to explain how the vulnerability is exploited, outline the potential business impact of a data breach, and list the two primary defensive strategies engineers use to prevent it.",
        "observation": "The 'Cybersecurity Expert' persona targets risk mitigation and executive reporting. Using analogies makes technical flaws clear for non-technical stakeholders while highlighting corporate impact."
    }
]
