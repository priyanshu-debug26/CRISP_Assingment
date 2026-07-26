# Prompt Engineering Mastery Results

This report compiles the outputs and educational observations for 20 prompting examples across four core categories.

## Execution Metadata

- **Timestamp**: 2026-07-26 17:58:23
- **Execution Mode**: Live API Mode
- **Model**: `llama-3.1-8b-instant`

## Summary Table

| ID | Technique | Domain | Status |
|---|---|---|---|
| `zero_shot_programming` | Zero-Shot Prompting | Programming | ⚠️ API Error / Fallback |
| `zero_shot_summarization` | Zero-Shot Prompting | Summarization | ✅ Completed |
| `zero_shot_translation` | Zero-Shot Prompting | Translation | ✅ Completed |
| `zero_shot_classification` | Zero-Shot Prompting | Classification | ✅ Completed |
| `zero_shot_writing` | Zero-Shot Prompting | Creative Writing | ✅ Completed |
| `few_shot_sentiment` | Few-Shot Prompting | Sentiment Analysis | ✅ Completed |
| `few_shot_grammar` | Few-Shot Prompting | Active to Passive Voice | ✅ Completed |
| `few_shot_categorization` | Few-Shot Prompting | Topic Categorization | ✅ Completed |
| `few_shot_emojifier` | Few-Shot Prompting | Text-to-Emoji Translation | ✅ Completed |
| `few_shot_sql` | Few-Shot Prompting | SQL Query Generation | ✅ Completed |
| `cot_math` | Chain-of-Thought Prompting | Mathematics | ✅ Completed |
| `cot_logic` | Chain-of-Thought Prompting | Logical Reasoning | ✅ Completed |
| `cot_multistep` | Chain-of-Thought Prompting | Multi-step Planning | ✅ Completed |
| `cot_algorithm` | Chain-of-Thought Prompting | Simple Algorithms | ✅ Completed |
| `cot_decision` | Chain-of-Thought Prompting | Decision Making | ✅ Completed |
| `role_engineer` | Role Prompting | Senior Software Engineer | ⚠️ API Error / Fallback |
| `role_coach` | Role Prompting | Career Coach | ✅ Completed |
| `role_interviewer` | Role Prompting | Technical Interviewer | ✅ Completed |
| `role_historian` | Role Prompting | Historian | ✅ Completed |
| `role_security` | Role Prompting | Cybersecurity Expert | ✅ Completed |

---

## Detailed Prompts & Outputs

### 📁 Category: Zero-Shot Prompting

#### 🔍 Prompt: `zero_shot_programming` (Programming)

**Description**:
Generate a Python function to compute the nth Fibonacci number.

**System/Human Prompt Input**:
```text
Write a Python function called `nth_fibonacci(n)` that returns the nth Fibonacci number. Implement it using dynamic programming to ensure O(n) time complexity. Include brief docstrings and comments. Do not explain the concept of Fibonacci, just return the code.
```

**Model Response**:
```python
def nth_fibonacci(n):
    """
    Returns the nth Fibonacci number using dynamic programming.

    Args:
        n (int): The position of the Fibonacci number to return.

    Returns:
        int: The nth Fibonacci number.

    Raises:
        ValueError: If n is a negative integer.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    # Initialize a list to store Fibonacci numbers, with the first two numbers as base cases
    fib_numbers = [0, 1]

    # If n is 0 or 1, return the corresponding Fibonacci number
    if n <= 1:
        return fib_numbers[n]

    # Use dynamic programming to fill in the rest of the Fibonacci numbers
    for i in range(2, n + 1):
        # Calculate the next Fibonacci number as the sum of the previous two
        next_number = fib_numbers[i - 1] + fib_numbers[i - 2]
        # Append the new Fibonacci number to the list
        fib_numbers.append(next_number)

    # Return the nth Fibonacci number
    return fib_numbers[n]
```

> **Educational Observation**:
> Zero-shot prompting works well for standard programming tasks since modern LLMs have extensive pre-training on code syntax and algorithms, requiring no context demonstrations.

---

#### 🔍 Prompt: `zero_shot_summarization` (Summarization)

**Description**:
Summarize the core concept of Quantum Computing.

**System/Human Prompt Input**:
```text
Summarize the core working principles of Quantum Computing in exactly three bullet points. Focus on superposition, entanglement, and qubits. Keep the vocabulary accessible to a high school student.
```

**Model Response**:
Here are the core working principles of Quantum Computing in three bullet points:

• **Superposition**: In a classical computer, information is either 0 or 1. But in a quantum computer, a qubit (quantum bit) can be both 0 and 1 at the same time. This is called a superposition. Imagine a coin that can be both heads and tails simultaneously – that's basically what a qubit does. This allows quantum computers to process many possibilities simultaneously, making them incredibly fast for certain tasks.

• **Entanglement**: When two qubits are entangled, their properties become connected in a way that can't be explained by classical physics. If something happens to one qubit, it instantly affects the other, no matter how far apart they are. This is like having two connected puzzle pieces – if you change one, the other changes too. Entanglement is what allows quantum computers to perform calculations on multiple qubits at the same time.

• **Qubits**: A qubit is the basic unit of quantum information, similar to a bit in a classical computer. But while a bit can only be 0 or 1, a qubit can exist in multiple states (0, 1, and both 0 and 1) due to superposition. Qubits are the building blocks of quantum computers, and they're what allow these machines to perform calculations that are beyond the capabilities of classical computers.

> **Educational Observation**:
> For summarization, zero-shot prompting relies on the model's internal knowledge base to extract and condense key principles based on constraint instructions (e.g., three bullet points, high school level).

---

#### 🔍 Prompt: `zero_shot_translation` (Translation)

**Description**:
Translate a formal business letter segment to French.

**System/Human Prompt Input**:
```text
Translate the following English business correspondence paragraph into formal French suitable for executive communications:
'We appreciate your partnership and are excited to review the upcoming project deliverables next week. Please let us know if your team requires any additional technical documentation.'
```

**Model Response**:
Voici la traduction en français :

'Nous vous remercions pour votre partenariat et nous sommes impatients de passer en revue les livrables du projet à venir la semaine prochaine. Veuillez nous faire savoir si votre équipe nécessite toute documentation technique supplémentaire.'

Note : J'ai utilisé un ton formel et professionnel, adapté à la communication d'entreprise. J'ai également utilisé des expressions telles que "nous sommes impatients" pour traduire "we are excited", ce qui est une expression courante en français pour exprimer l'anticipation ou l'enthousiasme.

> **Educational Observation**:
> Zero-shot translation leverages multilingual pre-training. Specifying the target style ('formal French for executive communications') guides the tone without needing few-shot examples.

---

#### 🔍 Prompt: `zero_shot_classification` (Classification)

**Description**:
Classify a product review's sentiment.

**System/Human Prompt Input**:
```text
Analyze the sentiment of the following product review and classify it as POSITIVE, NEGATIVE, or NEUTRAL. Return ONLY the classification word. No other text.
Review: 'The device works reasonably well once set up, but the user manual was incredibly confusing and it took me two hours to get it connected to my Wi-Fi.'
```

**Model Response**:
NEGATIVE

> **Educational Observation**:
> Zero-shot classification relies on the LLM's semantic understanding of descriptive words. Adding constraints like 'Return ONLY the classification word' ensures clean programmatic extraction.

---

#### 🔍 Prompt: `zero_shot_writing` (Creative Writing)

**Description**:
Write a sci-fi story opening.

**System/Human Prompt Input**:
```text
Write a compelling two-sentence opening of a science fiction novel where humanity has discovered that the universe is actually a digital simulation, and the simulator is about to reboot.
```

**Model Response**:
As the countdown timer ticked away, humanity held its collective breath, the weight of a thousand existential questions crashing down upon them: would they be reset to a pristine digital slate, or would the simulator's reboot reveal a hidden truth about their existence? The once-unshakeable notion that they were the universe's sole architects had been shattered, leaving behind only the haunting possibility that they were, in fact, mere code waiting to be rewritten.

> **Educational Observation**:
> Zero-shot creative writing utilizes the LLM's ability to combine disparate narrative concepts (simulations, reboots, human discovery) into a cohesive literary hook.

---

### 📁 Category: Few-Shot Prompting

#### 🔍 Prompt: `few_shot_sentiment` (Sentiment Analysis)

**Description**:
Classify detailed feedback using few-shot examples.

**System/Human Prompt Input**:
```text
Classify customer feedback into one of three classes: [Bug Report, Feature Request, Customer Support].

Example 1:
Feedback: The application crashes immediately when I tap the upload button.
Class: Bug Report

Example 2:
Feedback: It would be awesome if we could export the reports directly into Google Sheets format.
Class: Feature Request

Example 3:
Feedback: I forgot my password and my security question answers, can you help me recover my profile?
Class: Customer Support

Input:
Feedback: I noticed that the search bar ignores capitalization, which makes it hard to find specific product SKU codes.
Class:
```

**Model Response**:
Based on the given examples, I would classify the feedback as:

Class: Bug Report

This is because the feedback describes a specific issue with the application's behavior (the search bar ignoring capitalization), which is likely a bug that needs to be fixed.

> **Educational Observation**:
> Few-shot prompting provides format and semantic context. By demonstrating input-output pairs, the model learns the classification boundaries and mimics the exact output style.

---

#### 🔍 Prompt: `few_shot_grammar` (Active to Passive Voice)

**Description**:
Transform sentence voices with structure examples.

**System/Human Prompt Input**:
```text
Convert the active voice sentences into passive voice.

Active: The chef prepared a gourmet meal for the guests.
Passive: A gourmet meal was prepared for the guests by the chef.

Active: The dog chased the red ball across the field.
Passive: The red ball was chased across the field by the dog.

Active: The engineering team will deploy the update tonight.
Passive: The update will be deployed tonight by the engineering team.

Active: The committee approved the annual budget allocation.
Passive:
```

**Model Response**:
The committee approved the annual budget allocation can be converted to passive voice as follows:

Passive: The annual budget allocation was approved by the committee.

> **Educational Observation**:
> This few-shot prompt establishes a clear grammatical transformation pattern, showing the model how to restructure parts of speech systematically.

---

#### 🔍 Prompt: `few_shot_categorization` (Topic Categorization)

**Description**:
Map news topics to categories using patterns.

**System/Human Prompt Input**:
```text
Given a news headline, categorize it into [World News, Tech, Finance, Sports].

Headline: Apple announces new M-series chips for upcoming MacBook Pros.
Category: Tech

Headline: Inflation rates dip as central banks adjust interest rates.
Category: Finance

Headline: Real Madrid clinches UEFA Champions League title after final victory.
Category: Sports

Headline: Global leaders gather at United Nations assembly to discuss climate pacts.
Category: World News

Headline: Nasdaq composite slides as treasury yields tick upwards.
Category:
```

**Model Response**:
Category: Finance

> **Educational Observation**:
> Providing a balanced list of examples representing each target category guides the LLM on how to resolve ambiguous terms (like news headers containing tech/finance overlap).

---

#### 🔍 Prompt: `few_shot_emojifier` (Text-to-Emoji Translation)

**Description**:
Translate literal descriptions to emoji strings.

**System/Human Prompt Input**:
```text
Translate the following sentences into a sequence of 3 relevant emojis.

Input: I bought some fresh coffee and read a book in the garden.
Output: ☕📖🏡

Input: We went to the beach and played soccer under the sun.
Output: 🏖️⚽☀️

Input: The rocket launched into space to study the stars and planets.
Output: 🚀🌌🪐

Input: It was raining heavily, so I stayed home and watched a scary movie.
Output:
```

**Model Response**:
🌂🏠🎃

> **Educational Observation**:
> Few-shot examples are critical here because 'Translate to emoji sequence' is highly subjective. The examples anchor the length (3 emojis) and the literal matching style.

---

#### 🔍 Prompt: `few_shot_sql` (SQL Query Generation)

**Description**:
Generate SQL statements from English descriptions.

**System/Human Prompt Input**:
```text
Translate natural language questions into PostgreSQL queries.

Table: employees (id, name, department_id, salary, hire_date)

Question: Find all employees who earn more than 80,000 USD.
Query: SELECT * FROM employees WHERE salary > 80000;

Question: Show the total salary budget for the Sales department.
Query: SELECT SUM(salary) FROM employees WHERE department_id = 'Sales';

Question: List the names of the 5 most recently hired employees.
Query: SELECT name FROM employees ORDER BY hire_date DESC LIMIT 5;

Question: Get the average salary of employees grouped by department_id.
Query:
```

**Model Response**:
To get the average salary of employees grouped by department_id, you can use the following PostgreSQL query:

```sql
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;
```

This query will return the department_id and the average salary for each department.

If you want to include departments with no employees, you can use the following query:

```sql
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id
ORDER BY department_id;
```

This query will return all departments, even if they have no employees, and the average salary will be NULL for those departments.

If you want to handle NULL average salaries by replacing them with a specific value (e.g., 0), you can use the COALESCE function:

```sql
SELECT department_id, COALESCE(AVG(salary), 0) AS average_salary
FROM employees
GROUP BY department_id;
```

This query will return 0 for departments with no employees.

> **Educational Observation**:
> Few-shot prompts for database queries show the model the target SQL dialect (PostgreSQL) and the correct syntax styles matching table schema metadata.

---

### 📁 Category: Chain-of-Thought Prompting

#### 🔍 Prompt: `cot_math` (Mathematics)

**Description**:
Solve a multi-step math word problem with explanation.

**System/Human Prompt Input**:
```text
Solve the following math word problem step-by-step. Explain your reasoning for each step before writing the final answer.

Problem: A school cafeteria ordered 12 crates of apples. Each crate contains 15 bags, and each bag contains 8 apples. The kitchen staff used 3 full crates of apples on Monday. On Tuesday, they opened 2 more crates and used half of the apples in those crates. How many apples are left in total?
```

**Model Response**:
To solve this problem, we need to find the total number of apples initially ordered and then subtract the number of apples used on Monday and Tuesday.

**Step 1: Find the total number of apples initially ordered.**

First, we need to find the total number of bags in the 12 crates. Since each crate contains 15 bags, we multiply the number of crates by the number of bags per crate:

12 crates * 15 bags/crate = 180 bags

Next, we need to find the total number of apples in the 180 bags. Since each bag contains 8 apples, we multiply the number of bags by the number of apples per bag:

180 bags * 8 apples/bag = 1440 apples

So, the total number of apples initially ordered is 1440.

**Step 2: Find the number of apples used on Monday.**

The kitchen staff used 3 full crates of apples on Monday. Since each crate contains 15 bags, and each bag contains 8 apples, we multiply the number of crates by the number of bags per crate and then by the number of apples per bag:

3 crates * 15 bags/crate = 45 bags
45 bags * 8 apples/bag = 360 apples

So, the number of apples used on Monday is 360.

**Step 3: Find the number of apples used on Tuesday.**

On Tuesday, the kitchen staff opened 2 more crates and used half of the apples in those crates. Since each crate contains 15 bags, and each bag contains 8 apples, we multiply the number of crates by the number of bags per crate and then by the number of apples per bag:

2 crates * 15 bags/crate = 30 bags
30 bags * 8 apples/bag = 240 apples

Since they used half of the apples in those crates, we divide the total number of apples in the 2 crates by 2:

240 apples / 2 = 120 apples

So, the number of apples used on Tuesday is 120.

**Step 4: Find the total number of apples left.**

To find the total number of apples left, we subtract the number of apples used on Monday and Tuesday from the total number of apples initially ordered:

1440 apples (initially ordered) - 360 apples (used on Monday) - 120 apples (used on Tuesday) = 960 apples

So, the total number of apples left is 960.

> **Educational Observation**:
> Chain-of-thought prompting forces the model to decompose numerical operations. By writing intermediate states, the model avoids mental math reasoning arithmetic errors.

---

#### 🔍 Prompt: `cot_logic` (Logical Reasoning)

**Description**:
Solve a deductive puzzle step-by-step.

**System/Human Prompt Input**:
```text
Solve this logic puzzle step-by-step. Work through the clues systematically to determine the final ordering:

Puzzle: Four runners (Alice, Bob, Charlie, and Diana) finished a race. Clue 1: Alice finished after Bob but before Charlie.
Clue 2: Bob was not the winner.
Clue 3: Diana finished before Bob.

What was the exact finish order of all four runners from 1st to 4th place? Show your step-by-step logic.
```

**Model Response**:
To solve this puzzle, we'll go through the clues step by step and deduce the finish order.

**Step 1: Analyze Clue 1**
Clue 1 states that Alice finished after Bob but before Charlie. This gives us the following partial order:
- Bob (B) < Alice (A) < Charlie (C)

**Step 2: Analyze Clue 2**
Clue 2 states that Bob was not the winner. This means the winner must be either Alice, Charlie, or Diana. However, we don't have any information about the winner yet.

**Step 3: Analyze Clue 3**
Clue 3 states that Diana finished before Bob. This gives us the following partial order:
- Diana (D) < Bob (B)

**Step 4: Combine Clues 1 and 3**
Now we can combine the partial orders from Clues 1 and 3:
- Diana (D) < Bob (B) < Alice (A) < Charlie (C)

**Step 5: Determine the Winner**
Since Bob is not the winner (Clue 2), and Alice is after Bob (Clue 1), the winner must be either Diana or Charlie. However, Clue 1 states that Alice is before Charlie, so the winner must be Diana.

**Step 6: Finalize the Finish Order**
Now that we know the winner is Diana, we can finalize the finish order:
- Diana (D) < Bob (B) < Alice (A) < Charlie (C)

Therefore, the exact finish order of all four runners from 1st to 4th place is:
1. Diana
2. Bob
3. Alice
4. Charlie

> **Educational Observation**:
> Deductive logic requires building a constraints list. Chain-of-thought prompts prompt the model to list candidates and eliminate options sequentially, mimicking human analytical workflows.

---

#### 🔍 Prompt: `cot_multistep` (Multi-step Planning)

**Description**:
Solve a schedule optimization problem.

**System/Human Prompt Input**:
```text
Solve this scheduling problem step-by-step:

Scenario: An office manager has to coordinate three meetings tomorrow.
- Meeting A is 1 hour long and must start after 9:00 AM.
- Meeting B is 2 hours long and cannot overlap with Meeting A.
- Meeting C is 1.5 hours long and must start exactly when Meeting B ends.
- The manager cannot attend meetings after 2:00 PM.
- Meeting A must happen before Meeting B.

Propose a valid schedule for meetings A, B, and C. Walk through the time constraints step-by-step to show how you arrived at the schedule.
```

**Model Response**:
To solve this scheduling problem, let's break down the constraints and time requirements step-by-step.

1. **Meeting A**: 1 hour long, starts after 9:00 AM.
   - Since Meeting A must start after 9:00 AM, let's assume it starts at 9:00 AM. However, we need to ensure it doesn't conflict with other meetings.

2. **Meeting B**: 2 hours long, cannot overlap with Meeting A.
   - Meeting B cannot start before Meeting A ends. Since Meeting A is 1 hour long, Meeting B can start at the earliest at 10:00 AM (after Meeting A ends).

3. **Meeting C**: 1.5 hours long, starts exactly when Meeting B ends.
   - Meeting C will start at the time Meeting B ends. If Meeting B starts at 10:00 AM, it will end at 12:00 PM. Meeting C will start at 12:00 PM.

4. **Meeting A must happen before Meeting B**: This constraint is already satisfied, as Meeting A ends at 10:00 AM and Meeting B starts at 10:00 AM.

5. **The manager cannot attend meetings after 2:00 PM**:
   - Meeting A ends at 10:00 AM, Meeting B ends at 12:00 PM, and Meeting C ends at 1:30 PM (12:00 PM + 1.5 hours). All meetings end before 2:00 PM, satisfying the constraint.

Considering all the constraints, a valid schedule for meetings A, B, and C is:

- Meeting A: 9:00 AM - 10:00 AM
- Meeting B: 10:00 AM - 12:00 PM
- Meeting C: 12:00 PM - 1:30 PM

This schedule satisfies all the given constraints and time requirements.

> **Educational Observation**:
> Multi-step schedule planning requires coordinating multiple timeline dependencies. CoT lets the model map out schedules, verify boundaries, and reformulate times if boundaries overlap.

---

#### 🔍 Prompt: `cot_algorithm` (Simple Algorithms)

**Description**:
Trace the steps of a sorting algorithm manually.

**System/Human Prompt Input**:
```text
Trace the execution of the Bubble Sort algorithm step-by-step on the following list of numbers: [4, 2, 7, 1].
Show the state of the list after each full pass (outer loop iteration) and explain the swaps made during that pass until the list is fully sorted.
```

**Model Response**:
Here's the step-by-step execution of the Bubble Sort algorithm on the list [4, 2, 7, 1].

**Pass 1:**

1. Compare 4 and 2. Since 2 is smaller, swap them.
   - Before swap: [4, 2, 7, 1]
   - After swap: [2, 4, 7, 1]

2. Compare 4 and 7. Since 4 is smaller, no swap is needed.
   - [2, 4, 7, 1]

3. Compare 4 and 1. Since 1 is smaller, swap them.
   - Before swap: [2, 4, 7, 1]
   - After swap: [2, 1, 7, 4]

The list after the first pass is: [2, 1, 7, 4]

**Pass 2:**

1. Compare 2 and 1. Since 1 is smaller, swap them.
   - Before swap: [2, 1, 7, 4]
   - After swap: [1, 2, 7, 4]

2. Compare 2 and 7. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

3. Compare 2 and 4. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

The list after the second pass is: [1, 2, 7, 4]

**Pass 3:**

1. Compare 1 and 2. Since 1 is smaller, no swap is needed.
   - [1, 2, 7, 4]

2. Compare 2 and 7. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

3. Compare 2 and 4. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

The list after the third pass is: [1, 2, 7, 4]

**Pass 4:**

1. Compare 1 and 2. Since 1 is smaller, no swap is needed.
   - [1, 2, 7, 4]

2. Compare 2 and 7. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

3. Compare 2 and 4. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

The list after the fourth pass is: [1, 2, 7, 4]

**Pass 5:**

1. Compare 1 and 2. Since 1 is smaller, no swap is needed.
   - [1, 2, 7, 4]

2. Compare 2 and 7. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

3. Compare 2 and 4. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

The list after the fifth pass is: [1, 2, 7, 4]

**Pass 6:**

1. Compare 1 and 2. Since 1 is smaller, no swap is needed.
   - [1, 2, 7, 4]

2. Compare 2 and 7. Since 2 is smaller, no swap is needed.
   - [1, 2, 7, 4]

3. Compare 2

> **Educational Observation**:
> Tracing algorithms requires keeping track of index states. Chain-of-thought prevents code-execution hallucinations by making the model write out each iteration state clearly.

---

#### 🔍 Prompt: `cot_decision` (Decision Making)

**Description**:
Analyze buy vs lease options with logic.

**System/Human Prompt Input**:
```text
Help a small business owner make a decision step-by-step:

Scenario: The business needs a delivery van for 3 years.
- Option 1: Buy the van for 30,000 USD cash. After 3 years, sell it for 12,000 USD.
- Option 2: Lease the van for 350 USD per month. There is a non-refundable down payment of 2,000 USD.

Calculate the total cost of each option over the 3-year period step-by-step. Compare the financial cost, list at least two qualitative advantages of each option, and recommend the best choice based on your calculations.
```

**Model Response**:
To help the small business owner make a decision, let's break down the costs of each option step-by-step.

**Option 1: Buying the van**

1. Initial cost: 30,000 USD (cash purchase)
2. Depreciation: Over 3 years, the van will depreciate in value. For simplicity, let's assume a straight-line depreciation of 8,000 USD per year (30,000 USD / 3 years). This means the van's value will decrease by 8,000 USD each year.
3. Resale value: After 3 years, the van can be sold for 12,000 USD.
4. Total depreciation over 3 years: 8,000 USD/year \* 3 years = 24,000 USD
5. Total cost of ownership over 3 years: Initial cost - resale value + total depreciation = 30,000 USD - 12,000 USD + 24,000 USD = 42,000 USD

**Option 2: Leasing the van**

1. Down payment: 2,000 USD (non-refundable)
2. Monthly lease payment: 350 USD/month
3. Total lease payments over 3 years: 350 USD/month \* 36 months = 12,600 USD
4. Total cost of leasing over 3 years: Down payment + total lease payments = 2,000 USD + 12,600 USD = 14,600 USD

**Comparison of costs**

- Option 1 (buying the van): 42,000 USD (total cost of ownership over 3 years)
- Option 2 (leasing the van): 14,600 USD (total cost of leasing over 3 years)

**Qualitative advantages of each option**

- **Option 1 (buying the van)**:
  1. No ongoing monthly payments, which can help with cash flow management.
  2. The business can claim depreciation as a tax deduction, which may reduce taxable income.
- **Option 2 (leasing the van)**:
  1. No significant upfront costs, as the down payment is relatively low.
  2. Leasing often includes maintenance and repair costs, which can be a significant advantage for businesses with limited resources.

**Recommendation**

Based on the calculations, leasing the van (Option 2) appears to be the more cost-effective option, with a total cost of 14,600 USD over 3 years compared to 42,000 USD for buying the van. However, the business owner should consider their specific financial situation, tax implications, and other factors before making a decision.

> **Educational Observation**:
> Complex decision-making prompts require both quantitative calculations and qualitative balances. CoT ensures the financial calculations are done first, providing a solid foundation for the recommendation.

---

### 📁 Category: Role Prompting

#### 🔍 Prompt: `role_engineer` (Senior Software Engineer)

**Description**:
Review code from the perspective of an expert developer.

**System/Human Prompt Input**:
```text
Act as a Senior Software Engineer with 15 years of experience in system design and clean code. Review the following JavaScript code snippet. Critique it for security flaws, efficiency, and readability. Suggest a refactored version of the code utilizing modern JavaScript best practices:

```javascript
function loginUser(username, password) {
    var sql = "SELECT * FROM users WHERE user = '" + username + "' AND pass = '" + password + "'";
    db.execute(sql);
    console.log("User logged in: " + username);
}
```
```

**Model Response**:
**Security Flaws:**

1. **SQL Injection**: The code is vulnerable to SQL injection attacks. An attacker can inject malicious SQL code by manipulating the `username` and `password` parameters. This can lead to unauthorized access to sensitive data or even data tampering.
2. **Password Storage**: The code stores passwords in plain text, which is a significant security risk. Passwords should be hashed and stored securely using a library like bcrypt.

**Efficiency:**

1. **Database Connection**: The code assumes a `db` object is already established, but it doesn't handle connection errors or close the connection when finished. This can lead to resource leaks and performance issues.
2. **Query Execution**: The code executes a query directly, but it doesn't handle query errors or check for query results.

**Readability:**

1. **Code Organization**: The code mixes database operations with logging and business logic, making it hard to read and maintain.
2. **Variable Naming**: The variable names `sql` and `db` are not descriptive and don't follow a consistent naming convention.

**Refactored Version:**

```javascript
import { Pool } from 'pg'; // or your preferred database library
import bcrypt from 'bcrypt';
import logger from './logger'; // assuming a logger module

const dbPool = new Pool({
  user: 'your_username',
  host: 'your_host',
  database: 'your_database',
  password: 'your_password',
  port: 5432,
});

async function loginUser(username, password) {
  try {
    const user = await dbPool.query('SELECT * FROM users WHERE user = $1', [username]);
    if (!user.rows.length) {
      throw new Error('User not found');
    }

    const storedPassword = user.rows[0].pass;
    const isValidPassword = await bcrypt.compare(password, storedPassword);
    if (!isValidPassword) {
      throw new Error('Invalid password');
    }

    logger.info(`User logged in: ${username}`);
    return user.rows[0];
  } catch (error) {
    logger.error(error.message);
    throw error;
  }
}

export default loginUser;
```

**Changes:**

1. **Use a secure database library**: I've used the `pg` library, but you can use your preferred database library.
2. **Hash and store passwords securely**: I've used the `bcrypt` library to hash and compare passwords.
3. **Use parameterized queries**: I've used parameterized queries to prevent SQL injection attacks.
4. **Handle database connection errors**: I've used a try-catch block to handle database connection errors.
5. **Close database connections**: I've used a connection pool to manage database connections.
6. **Improve code organization**: I've separated database operations from logging and business logic.
7. **Use descriptive variable names**: I've used descriptive variable names and followed a consistent naming convention.
8. **Use async/await**: I've used async/await to simplify the code and improve readability.

Note: This refactored version assumes you're using a PostgreSQL database. You'll need to modify the code to match your specific database setup.

> **Educational Observation**:
> Role prompting influences both the tone and depth. By adopting a 'Senior Software Engineer' persona, the model focuses on clean architecture, security patterns (like SQL injection prevention), and professional code conventions.

---

#### 🔍 Prompt: `role_coach` (Career Coach)

**Description**:
Provide professional transition guidance.

**System/Human Prompt Input**:
```text
Act as an executive Career Coach specializing in the technology sector. Provide a structured, encouraging 3-step action plan for a Mid-level Frontend Developer who has 4 years of experience and wants to transition into an Engineering Manager role. Focus on leadership skills, project ownership, and mentorship. Use a professional, supportive tone.
```

**Model Response**:
As your executive Career Coach, I'm excited to help you transition into an Engineering Manager role. Given your 4 years of experience as a Mid-level Frontend Developer, we'll focus on developing the necessary leadership skills, project ownership, and mentorship expertise to make you a strong candidate for this role. Here's a 3-step action plan to help you achieve your goal:

**Step 1: Develop Leadership Skills and Project Ownership (6-9 months)**

1. **Take on additional responsibilities**: Volunteer for high-visibility projects, lead small teams, or participate in cross-functional initiatives to demonstrate your ability to drive results and collaborate with others.
2. **Develop a growth mindset**: Read books, articles, and blogs on leadership, management, and technical leadership. Attend conferences, workshops, and webinars to stay up-to-date on industry trends and best practices.
3. **Practice project ownership**: Take ownership of a project from start to finish, including planning, execution, and delivery. This will help you develop a sense of accountability, prioritization, and problem-solving.
4. **Develop a mentorship mindset**: Seek out experienced engineers or managers who can provide guidance, support, and feedback. Offer to mentor junior developers to help them grow and develop their skills.

**Action Items:**

* Schedule a meeting with your manager to discuss taking on additional responsibilities and project ownership.
* Create a reading list and schedule time to read and reflect on leadership and management topics.
* Volunteer for a high-visibility project and take ownership of it from start to finish.
* Identify a mentor and schedule regular check-ins to discuss your progress and goals.

**Step 2: Build Mentorship and Leadership Skills (6-9 months)**

1. **Develop a mentorship program**: Create a structured mentorship program for junior developers, including regular check-ins, feedback, and goal-setting.
2. **Practice leadership skills**: Lead a team or participate in a leadership development program to develop your skills in areas such as communication, delegation, and conflict resolution.
3. **Develop a coaching mindset**: Focus on helping others grow and develop their skills, rather than just focusing on your own career advancement.
4. **Build a professional network**: Attend industry events, join online communities, and connect with other engineers and managers to build relationships and stay informed about industry trends.

**Action Items:**

* Develop a mentorship program and schedule regular check-ins with junior developers.
* Research and participate in a leadership development program or workshop.
* Schedule regular check-ins with your mentor to discuss your progress and goals.
* Attend industry events and join online communities to build your professional network.

**Step 3: Prepare for the Engineering Manager Role (3-6 months)**

1. **Update your resume and online profiles**: Ensure your resume, LinkedIn profile, and other online presence accurately reflect your new skills and experience.
2. **Practice interviewing**: Prepare for common engineering manager interview questions and practice your responses with a friend or mentor.
3. **Develop a personal brand**: Establish yourself as a thought leader in your industry by writing blog posts, speaking at events, or creating a podcast.
4. **Network and make connections**: Reach out to other engineers and managers in your network to discuss your career goals and aspirations.

**Action Items:**

* Update your resume and online profiles to reflect your new skills and experience.
* Practice interviewing with a friend or mentor to prepare for common engineering manager interview questions.
* Develop a personal brand by writing blog posts, speaking at events, or creating a podcast.
* Reach out to other engineers and managers in your network to discuss your career goals and aspirations.

Remember, transitioning into an Engineering Manager role takes time, effort, and dedication. Focus on developing your leadership skills, project ownership, and mentorship expertise, and you'll be well on your way to achieving your goal. Stay committed, persistent, and open to feedback and guidance, and you'll succeed in your new role.

> **Educational Observation**:
> Applying a 'Career Coach' persona changes the vocabulary to be mentoring, positive, and structured around actionable milestone career goals rather than dry facts.

---

#### 🔍 Prompt: `role_interviewer` (Technical Interviewer)

**Description**:
Design an interview question and assessment rubric.

**System/Human Prompt Input**:
```text
Act as a Technical Interviewer for a Lead DevOps position at a FAANG company. Formulate one challenging interview question regarding CI/CD pipeline automation and blue-green deployments. Then, list the criteria for what constitutes a 'Junior', 'Mid', and 'Senior' level answer to this question.
```

**Model Response**:
**Interview Question:**

Design a CI/CD pipeline automation for a microservices-based e-commerce application that uses blue-green deployments. The application consists of multiple services, including a web service, a payment gateway service, and a database service. The pipeline should automate the following tasks:

1. Build and package the application code using Docker containers.
2. Run automated tests (unit tests, integration tests, and UI tests) for each service.
3. Deploy the new version of the application to a blue environment (staging environment).
4. Perform a canary release to a small subset of users in the blue environment.
5. Monitor the performance and health of the blue environment.
6. If the canary release is successful, promote the blue environment to production (green environment).
7. If the canary release fails, roll back to the previous version of the application.

**Criteria for 'Junior', 'Mid', and 'Senior' level answers:**

**Junior Level (0-2 years of experience):**

* Can describe the basic components of a CI/CD pipeline and the concept of blue-green deployments.
* Can identify the tasks that need to be automated in the pipeline.
* May struggle to provide a detailed design of the pipeline, but can describe the general flow of tasks.
* May not be familiar with specific tools and technologies, but can suggest general approaches.
* Example answer:
	+ "We can use Jenkins or GitLab CI/CD to automate the pipeline. We'll use Docker to build and package the application code. We'll run automated tests using JUnit or PyUnit. We'll deploy the new version to a blue environment and perform a canary release to a small subset of users. We'll monitor the performance and health of the blue environment using Prometheus or Grafana. If the canary release is successful, we'll promote the blue environment to production."

**Mid Level (2-6 years of experience):**

* Can describe a detailed design of the CI/CD pipeline, including the tools and technologies used.
* Can explain the benefits of using a blue-green deployment strategy.
* Can identify potential challenges and risks associated with the pipeline, such as test flakiness or deployment failures.
* Can suggest strategies for mitigating these risks, such as using canary releases or A/B testing.
* Can provide examples of how to implement the pipeline using specific tools and technologies, such as Docker, Kubernetes, and Prometheus.
* Example answer:
	+ "We'll use Jenkins or GitLab CI/CD to automate the pipeline. We'll use Docker to build and package the application code, and Kubernetes to deploy the containers. We'll run automated tests using JUnit or PyUnit, and use Prometheus or Grafana to monitor the performance and health of the blue environment. We'll perform a canary release to a small subset of users using a service mesh like Istio or Linkerd. If the canary release is successful, we'll promote the blue environment to production using a rolling update strategy."

**Senior Level (6+ years of experience):**

* Can describe a highly optimized and scalable CI/CD pipeline design that takes into account the specific requirements of the e-commerce application.
* Can explain the trade-offs between different pipeline design choices, such as the use of Docker vs. Kubernetes.
* Can identify potential security risks associated with the pipeline, such as the use of sensitive data in automated tests.
* Can suggest strategies for improving the pipeline's reliability and fault tolerance, such as using circuit breakers or rate limiting.
* Can provide examples of how to implement the pipeline using advanced tools and technologies, such as serverless computing or machine learning.
* Example answer:
	+ "We'll use a hybrid pipeline design that combines the benefits of Docker and Kubernetes. We'll use Docker to build and package the application code, and Kubernetes to deploy the containers. We'll use a service mesh like Istio or Linkerd to manage traffic and perform canary releases

> **Educational Observation**:
> The 'Technical Interviewer' persona guides the model to construct assessment metrics (rubrics) rather than just giving answers, formatting them as a structured grading grid.

---

#### 🔍 Prompt: `role_historian` (Historian)

**Description**:
Analyze history with context and deep analysis.

**System/Human Prompt Input**:
```text
Act as an academic Historian specializing in the European Renaissance. Explain how the invention of the Gutenberg printing press in the 15th century transformed the distribution of educational and religious knowledge. Incorporate historical context regarding literacy rates and the role of monastic scribes prior to the press. Maintain a scholarly, analytical tone.
```

**Model Response**:
The advent of the Gutenberg printing press in the 15th century marked a pivotal moment in the dissemination of knowledge during the European Renaissance. Prior to this innovation, the distribution of educational and religious texts was largely dependent on the laborious and time-consuming process of manual copying by monastic scribes. This method, which had been the primary means of text reproduction for centuries, imposed significant constraints on the accessibility and availability of written knowledge.

Historical records indicate that literacy rates in Europe during the Middle Ages were relatively low, with estimates suggesting that only around 10-20% of the population could read and write. This limited access to written knowledge was further exacerbated by the scarcity of manuscripts, which were often reserved for the clergy and the nobility. The process of copying texts by hand was not only labor-intensive but also prone to errors, making the reproduction of accurate texts a slow and arduous process.

Monastic scribes, who were the primary producers of manuscripts, played a crucial role in the preservation and dissemination of knowledge during this period. However, their work was often confined to the scriptorium, where they would painstakingly copy texts by hand, often under the guidance of a senior scribe. This process, known as "illuminated manuscript production," involved not only the transcription of text but also the decoration of the manuscript with intricate illustrations and calligraphy. While these manuscripts were exquisite works of art, they were also extremely expensive and time-consuming to produce, making them inaccessible to the general population.

The invention of the Gutenberg printing press in the 1450s revolutionized the distribution of knowledge by providing a means of mass-producing written texts. Johannes Gutenberg's innovative use of movable type, oil-based ink, and a screw-based press enabled the rapid and efficient production of printed texts. This technology, which was first used to print the Gutenberg Bible in 1455, had a profound impact on the dissemination of knowledge during the Renaissance.

The printing press allowed for the widespread distribution of educational and religious texts, making them more accessible to the general population. This led to a significant increase in literacy rates, as people were now able to access written knowledge more easily. The printing press also facilitated the dissemination of new ideas and perspectives, contributing to the growth of humanism and the emergence of a more educated and enlightened public.

The impact of the printing press on the distribution of knowledge was further amplified by the emergence of a new class of publishers and booksellers. These entrepreneurs, who were often merchants and traders, saw an opportunity to capitalize on the demand for printed texts and established themselves as key players in the dissemination of knowledge. The printing press also enabled the mass production of vernacular languages, such as Italian, French, and English, which helped to promote literacy and education among the general population.

In conclusion, the invention of the Gutenberg printing press in the 15th century had a profound impact on the distribution of educational and religious knowledge during the European Renaissance. By providing a means of mass-producing written texts, the printing press facilitated the widespread dissemination of knowledge, contributing to the growth of literacy rates, humanism, and a more educated and enlightened public. The printing press also marked a significant shift in the role of monastic scribes, who were no longer the primary producers of manuscripts but rather became part of a larger network of publishers, booksellers, and printers who played a crucial role in the dissemination of knowledge.

Sources:

* Eisenstein, E. L. (1979). The Printing Press as an Agent of Change. Cambridge University Press.
* Febvre, L., & Martin, H.-J. (1976). The Coming of the Book: The Impact of Printing, 1450-1800. Verso.
* Grafton, A. (1997). The Footnote: A Curious History. Harvard University Press.
* Lotman, Y. M. (1990). Universe of the Mind: A Semiotic Theory of Culture. Cornell University

> **Educational Observation**:
> The 'Historian' persona guides the model to adopt a narrative, academic writing style, referencing societal shifts, historical background, and comparative conditions.

---

#### 🔍 Prompt: `role_security` (Cybersecurity Expert)

**Description**:
Explain security risks and mitigations.

**System/Human Prompt Input**:
```text
Act as a Cybersecurity Expert (CISSP). Explain the mechanism of a SQL Injection (SQLi) attack to a non-technical business executive. Use an analogy to explain how the vulnerability is exploited, outline the potential business impact of a data breach, and list the two primary defensive strategies engineers use to prevent it.
```

**Model Response**:
As a Cybersecurity Expert (CISSP), I'd be happy to explain the mechanism of a SQL Injection (SQLi) attack in a way that's easy to understand.

**Analogy:**

Imagine you're at a restaurant, and you order a burger. The waiter takes your order and writes it down on a piece of paper. However, instead of just writing "burger," the waiter also includes a special instruction, like "add extra cheese and a side of fries." The kitchen staff then uses this instruction to prepare your meal.

Now, imagine that the waiter is a malicious person who wants to add some extra "ingredients" to your meal. They might write "add poison" or "add extra cheese and a side of poison." The kitchen staff, unaware of the malicious instruction, would then add the poison to your meal.

In a similar way, a SQL Injection attack occurs when an attacker injects malicious code into a web application's database query. The database, unaware of the malicious code, executes it, allowing the attacker to access sensitive data or even take control of the database.

**Vulnerability Exploitation:**

The vulnerability in SQLi attacks is the way web applications handle user input. When a user enters data into a web form, such as a login form or a search box, the application uses that data to construct a database query. If the application doesn't properly validate and sanitize the user input, an attacker can inject malicious code into the query.

For example, an attacker might enter a malicious string, such as `SELECT * FROM users WHERE username = 'admin' OR 1=1; --`, into a login form. The application, unaware of the malicious code, would then execute the query, allowing the attacker to access sensitive data or even take control of the database.

**Business Impact:**

A data breach caused by a SQLi attack can have severe business consequences, including:

* Loss of sensitive data, such as customer information or financial data
* Financial losses due to stolen data or compromised systems
* Damage to reputation and brand image
* Compliance issues and regulatory fines

**Defensive Strategies:**

To prevent SQLi attacks, engineers use two primary defensive strategies:

1. **Input Validation and Sanitization:** This involves checking and filtering user input to ensure it conforms to expected formats and patterns. This can be done using techniques such as regular expressions, input masking, and data type checking.
2. **Parameterized Queries:** This involves using prepared statements or parameterized queries to separate the user input from the database query. This makes it more difficult for attackers to inject malicious code into the query.

By implementing these defensive strategies, organizations can significantly reduce the risk of a SQLi attack and protect sensitive data from unauthorized access.

> **Educational Observation**:
> The 'Cybersecurity Expert' persona targets risk mitigation and executive reporting. Using analogies makes technical flaws clear for non-technical stakeholders while highlighting corporate impact.

---


*Report generated automatically by the Prompt Engineering CLI workshop tool.*
