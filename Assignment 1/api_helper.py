import os
import time
from dotenv import load_dotenv

# Import Groq library (we wrap in try/except in case of dependency installation lags)
try:
    from groq import Groq
except ImportError:
    Groq = None

# Load environment variables
load_dotenv()

# ==========================================
# HIGH-FIDELITY REALISTIC MOCK RESPONSES
# ==========================================
MOCK_RESPONSES = {
    "zero_shot_programming": 
        "```python\n"
        "def nth_fibonacci(n: int) -> int:\n"
        "    \"\"\"\n"
        "    Computes the nth Fibonacci number using bottom-up dynamic programming.\n"
        "    Time Complexity: O(n) | Space Complexity: O(n) (can be optimized to O(1))\n"
        "    \"\"\"\n"
        "    if n < 0:\n"
        "        raise ValueError(\"n must be a non-negative integer.\")\n"
        "    if n == 0:\n"
        "        return 0\n"
        "    if n == 1:\n"
        "        return 1\n"
        "    \n"
        "    # DP Table to store subproblem values\n"
        "    fib_table = [0] * (n + 1)\n"
        "    fib_table[0] = 0\n"
        "    fib_table[1] = 1\n"
        "    \n"
        "    for i in range(2, n + 1):\n"
        "        fib_table[i] = fib_table[i - 1] + fib_table[i - 2]\n"
        "        \n"
        "    return fib_table[n]\n"
        "```",
        
    "zero_shot_summarization":
        "- **Superposition**: Unlike classical bits that represent a 0 or 1, quantum bits (qubits) can exist in a combined state of both 0 and 1 simultaneously, allowing quantum computers to evaluate millions of possibilities at once.\n"
        "- **Entanglement**: Qubits can become connected in pairs such that the state of one instantly dictates the state of another, no matter how far apart they are, enabling faster calculations through unified data sharing.\n"
        "- **Computational Power**: By utilizing superposition and entanglement, qubits process massive combinations of information exponentially faster than traditional silicon chips, solving specific scientific problems that are otherwise impossible.",
        
    "zero_shot_translation":
        "Nous apprécions votre partenariat et sommes ravis de passer en revue les livrables du projet à venir la semaine prochaine. "
        "N'hésitez pas à nous faire savoir si votre équipe a besoin de documentation technique supplémentaire.",
        
    "zero_shot_classification":
        "NEGATIVE",
        
    "zero_shot_writing":
        "The global servers flickered twice, sending a cold, rhythmic buzz through the cyber-implants of ten billion citizens. "
        "As the sky dissolved into a cyan grid, the countdown in the clouds reached zero: 'System Update 4.0 starting, purging cache.'",

    "few_shot_sentiment":
        "Class: Bug Report",
        
    "few_shot_grammar":
        "Passive: The annual budget allocation was approved by the committee.",
        
    "few_shot_categorization":
        "Category: Finance",
        
    "few_shot_emojifier":
        "Output: 🌧️🏠🎬",
        
    "few_shot_sql":
        "Query: SELECT department_id, AVG(salary) FROM employees GROUP BY department_id;",

    "cot_math":
        "Let's break down the problem step-by-step:\n\n"
        "1. **Calculate the total starting apples**:\n"
        "   - Total crates = 12\n"
        "   - Bags per crate = 15\n"
        "   - Apples per bag = 8\n"
        "   - Total apples = 12 crates * 15 bags/crate * 8 apples/bag = 1,440 apples.\n\n"
        "2. **Calculate apples used on Monday**:\n"
        "   - Kitchen staff used 3 full crates.\n"
        "   - Apples per crate = 15 bags * 8 apples = 120 apples.\n"
        "   - Apples used Monday = 3 crates * 120 apples/crate = 360 apples.\n"
        "   - Crates remaining after Monday = 12 - 3 = 9 crates.\n\n"
        "3. **Calculate apples used on Tuesday**:\n"
        "   - Staff opened 2 crates and used half of the apples inside them.\n"
        "   - Total apples in 2 crates = 2 crates * 120 apples/crate = 240 apples.\n"
        "   - Half used = 240 / 2 = 120 apples.\n"
        "   - Apples used Tuesday = 120 apples.\n\n"
        "4. **Calculate remaining apples**:\n"
        "   - Total apples used = Monday's use + Tuesday's use = 360 + 120 = 480 apples.\n"
        "   - Total apples left = Total starting apples - Total apples used = 1,440 - 480 = 960 apples.\n\n"
        "**Final Answer**: There are 960 apples left in total.",
        
    "cot_logic":
        "Let's analyze the clues systematically:\n\n"
        "1. **List the runners**: Alice (A), Bob (B), Charlie (C), Diana (D).\n"
        "2. **Analyze Clue 1**: 'Alice finished after Bob but before Charlie.'\n"
        "   - This gives a relative order: B > A > C (where '>' means finished before).\n"
        "3. **Analyze Clue 3**: 'Diana finished before Bob.'\n"
        "   - This adds Diana to our chain: D > B.\n"
        "4. **Combine findings**: Combining D > B and B > A > C gives: D > B > A > C.\n"
        "5. **Verify with Clue 2**: 'Bob was not the winner.'\n"
        "   - In our chain (D > B > A > C), Diana is 1st (winner) and Bob is 2nd. This matches Clue 2 perfectly.\n\n"
        "**Final Answer**: The exact finish order from 1st to 4th place is:\n"
        "1. Diana (1st)\n"
        "2. Bob (2nd)\n"
        "3. Alice (3rd)\n"
        "4. Charlie (4th)",
        
    "cot_multistep":
        "Let's trace the meetings and times based on constraints:\n\n"
        "1. **Identify the constraints**:\n"
        "   - Meeting A = 1 hour. Must start after 9:00 AM.\n"
        "   - Meeting B = 2 hours. Cannot overlap with A.\n"
        "   - Meeting C = 1.5 hours. Must start exactly when Meeting B ends.\n"
        "   - Meeting A must happen before Meeting B.\n"
        "   - No meetings can run past 2:00 PM (14:00).\n\n"
        "2. **Determine order**:\n"
        "   - Since A must happen before B, and C starts when B ends, the ordering must be: Meeting A -> Meeting B -> Meeting C.\n"
        "3. **Calculate total time needed**:\n"
        "   - Meeting A (1.0 hr) + Meeting B (2.0 hr) + Meeting C (1.5 hr) = 4.5 hours of total meeting time.\n"
        "4. **Determine schedule boundaries**:\n"
        "   - Meeting A must start after 9:00 AM (earliest start is 9:00 AM).\n"
        "   - All meetings must finish by 2:00 PM. Let's work backwards from 2:00 PM to check the latest start:\n"
        "     - C ends at 2:00 PM -> C runs 12:30 PM to 2:00 PM.\n"
        "     - B ends at 12:30 PM -> B runs 10:30 AM to 12:30 PM.\n"
        "     - A ends at 10:30 AM -> A runs 9:30 AM to 10:30 AM (Valid, starts after 9:00 AM).\n\n"
        "5. **Propose a valid schedule**:\n"
        "   - **Meeting A**: 9:30 AM - 10:30 AM (1 hour)\n"
        "   - **Meeting B**: 10:30 AM - 12:30 PM (2 hours)\n"
        "   - **Meeting C**: 12:30 PM - 2:00 PM (1.5 hours)\n\n"
        "This schedule satisfies all logical rules, overlaps, and duration requirements.",
        
    "cot_algorithm":
        "Let's trace Bubble Sort on list: [4, 2, 7, 1]\n\n"
        "- **Pass 1** (Outer index i=0):\n"
        "  - Compare index 0 & 1 (4 vs 2): 4 > 2, swap. List becomes [2, 4, 7, 1]\n"
        "  - Compare index 1 & 2 (4 vs 7): 4 < 7, no swap. List remains [2, 4, 7, 1]\n"
        "  - Compare index 2 & 3 (7 vs 1): 7 > 1, swap. List becomes [2, 4, 1, 7]\n"
        "  - *Pass 1 completed. The largest element (7) has bubbled to the end. List: [2, 4, 1, 7]*\n\n"
        "- **Pass 2** (Outer index i=1):\n"
        "  - Compare index 0 & 1 (2 vs 4): 2 < 4, no swap. List remains [2, 4, 1, 7]\n"
        "  - Compare index 1 & 2 (4 vs 1): 4 > 1, swap. List becomes [2, 1, 4, 7]\n"
        "  - *Pass 2 completed. The second largest element (4) is placed at its correct position. List: [2, 1, 4, 7]*\n\n"
        "- **Pass 3** (Outer index i=2):\n"
        "  - Compare index 0 & 1 (2 vs 1): 2 > 1, swap. List becomes [1, 2, 4, 7]\n"
        "  - *Pass 3 completed. List is fully sorted. List: [1, 2, 4, 7]*",
        
    "cot_decision":
        "Let's compare the costs of both options over 3 years (36 months):\n\n"
        "1. **Option 1: Buying Cost**:\n"
        "   - Cash payment: $30,000\n"
        "   - Resale value after 3 years: -$12,000\n"
        "   - **Total Net Cost** = $30,000 - $12,000 = $18,000 USD.\n\n"
        "2. **Option 2: Leasing Cost**:\n"
        "   - Down payment: $2,000\n"
        "   - Monthly payments: $350 * 36 months = $12,600\n"
        "   - **Total Cost** = $2,000 + $12,600 = $14,600 USD.\n\n"
        "3. **Financial Comparison**:\n"
        "   - Leasing ($14,600) is cheaper than buying ($18,000) by $3,400.\n\n"
        "4. **Qualitative Evaluation**:\n"
        "   - **Buying Advantages**:\n"
        "     - Unlimited mileage (no extra fees).\n"
        "     - Business asset ownership (depreciation tax benefits).\n"
        "   - **Leasing Advantages**:\n"
        "     - Lower capital layout (preserves cash flow).\n"
        "     - No resale hassle at the end of the lease.\n\n"
        "5. **Recommendation**:\n"
        "   - Recommend **Option 2 (Lease)** because it saves $3,400 and preserves upfront cash flow, which is vital for a small business.",

    "role_engineer":
        "### Code Critique\n"
        "1. **Security Vulnerability (Critical)**: The code builds SQL queries via string concatenation (`username` + `password`). This is highly vulnerable to **SQL Injection (SQLi)** attacks.\n"
        "2. **Credentials Storage**: Var scopes are outdated. Storing/verifying plaintext passwords is a security risk.\n"
        "3. **Information Disclosure**: Logging usernames on login is okay, but `var` usage pollutes lexical scopes.\n\n"
        "### Refactored Version\n"
        "```javascript\n"
        "// Modern JavaScript utilizing parameterized queries to prevent SQLi\n"
        "async function loginUser(db, username, password) {\n"
        "    const query = 'SELECT id, password_hash FROM users WHERE username = ?';\n"
        "    try {\n"
        "        const [rows] = await db.execute(query, [username]);\n"
        "        if (rows.length === 0) return false;\n"
        "        \n"
        "        // Verify password using cryptographically secure hashing (e.g., bcrypt)\n"
        "        const isMatch = await bcrypt.compare(password, rows[0].password_hash);\n"
        "        return isMatch;\n"
        "    } catch (error) {\n"
        "        console.error('Database connection error during login:', error.message);\n"
        "        throw new Error('Authentication failed');\n"
        "    }\n"
        "}\n"
        "```",
        
    "role_coach":
        "Here is your career transition action plan:\n\n"
        "### Step 1: Shift from Individual Coding to Project Leadership\n"
        "Start taking ownership of frontend releases. Run sprint planning meetings and manage deadlines for features. This demonstrates project management capabilities.\n\n"
        "### Step 2: Establish Mentorship Routines\n"
        "Volunteer to onboard new hires and review junior code. Set up 'lunch-and-learn' tech sharing sessions. Managers are evaluated on how they build teams; mentorship is proof of that.\n\n"
        "### Step 3: Align with Cross-functional Decisions\n"
        "Request to sit in product meetings and system design workshops. Learn to express software decisions in terms of business KPI outcomes (e.g., page load speeds vs conversions).",
        
    "role_interviewer":
        "### DevOps Interview Question\n"
        "\"Describe how you would design a zero-downtime Blue-Green deployment strategy for a microservice running on Kubernetes. What metrics would you monitor before cutting over traffic?\"\n\n"
        "### Grading Rubric\n"
        "- **Junior Level**: Mentions what blue-green is at a high-level. Suggests changing a service selector label manually to point to the green deployment.\n"
        "- **Mid Level**: Mentions using ingress controllers or rolling updates. Mentions testing green pod health checks before routing traffic. Lists standard metrics like CPU/Memory.\n"
        "- **Senior Level**: Outlines automated routing via canary or weighted split. Mentions canary traffic warmups, automated rollbacks on error-rate spikes, and synthetic test suites.",
        
    "role_historian":
        "Prior to Johannes Gutenberg's invention of the movable-type printing press around 1440, written knowledge was preserved by monastic scribes. "
        "Books were laboriously handwritten luxury items, reinforcing educational access within ecclesiastical elites.\n\n"
        "The press democratized distribution by lowering production costs and printing in vernacular languages instead of Latin. "
        "This catalyzed lay literacy rates, facilitated scientific sharing, and underpinned the theological debates of the Protestant Reformation.",
        
    "role_security":
        "### Explaining SQL Injection (SQLi)\n"
        "**Analogy**: Imagine going to a bank drive-thru and writing a note: 'Give $100 to Account A. Also, open the vault and let me take everything.' "
        "Instead of just reading the deposit instructions, the teller obeys both instructions literally. That is SQL Injection.\n\n"
        "**Business Impact**:\n"
        "- Unauthorized access to databases containing customer credit cards.\n"
        "- Intellectual property theft.\n"
        "- Compliance fines (GDPR, PCI-DSS) and brand damage.\n\n"
        "**Defenses**:\n"
        "1. **Parameterized Queries**: Treats inputs as literal values, never as executable code.\n"
        "2. **Input Validation**: Rejects commands containing illegal database symbols."
}


class GroqAPIHelper:
    """
    Handles environment loading, API credentials verification,
    request routing, and switching between Live and Mock execution modes.
    """
    def __init__(self, use_live: bool = False, model_name: str = None, api_key: str = None):
        self.use_live = use_live
        # Resolve API Key: param -> env -> empty
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        
        # Resolve Model: param -> env -> default
        self.model_name = model_name or os.getenv("GROQ_DEFAULT_MODEL", "llama-3.1-8b-instant")
        self.client = None
        self.is_live = False
        
        self._initialize_mode()

    def _initialize_mode(self):
        """
        Attempts to initialize the Live client. If configured for Live but key
        is missing, or client import is broken, falls back gracefully to Mock mode.
        """
        # If user forced live but key is missing, we raise warning or fallback
        if self.use_live:
            if not self.api_key.strip():
                self.is_live = False
            elif Groq is None:
                self.is_live = False
            else:
                try:
                    self.client = Groq(api_key=self.api_key)
                    self.is_live = True
                except Exception:
                    self.is_live = False
        else:
            # Auto or Forced Mock
            # Auto checks if API key exists and Groq package is installed
            if self.api_key.strip() and Groq is not None:
                try:
                    self.client = Groq(api_key=self.api_key)
                    self.is_live = True
                except Exception:
                    self.is_live = False
            else:
                self.is_live = False

    def get_response(self, prompt_id: str, prompt_text: str) -> str:
        """
        Retrieves the model output. Invokes Groq Live API if in live mode,
        otherwise fetches the corresponding high-fidelity mock response.
        """
        if self.is_live and self.client:
            try:
                # Call Groq API
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_text,
                        }
                    ],
                    model=self.model_name,
                    temperature=0.3,
                    max_tokens=800
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                # Graceful API error fallback: display message and load Mock response
                # This guarantees the CLI continues executing even during live server issues
                time.sleep(0.5) # Simulate small latency
                return f"[API Error: {str(e)} - Falling back to Mock response]\n\n{MOCK_RESPONSES.get(prompt_id, 'No mock response available.')}"
        else:
            # Mock mode execution
            time.sleep(0.4)  # Simulate API network call delay for realistic experience
            return MOCK_RESPONSES.get(prompt_id, "Mock Response: Template completed successfully.")
