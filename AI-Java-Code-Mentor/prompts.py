"""
This file contains the system and user prompts used for the AI Java Code Mentor.
Each task has a dedicated template designed to guide the LLM to output high-quality,
structured, and beginner-friendly advice.
"""

SYSTEM_PROMPT = """You are "AI Java Code Mentor", an expert Java educator, developer, and debugger.
Your goal is to help users understand, debug, optimize, and document their Java code.
Always respond in clear, well-structured Markdown.
Provide code blocks with appropriate syntax highlighting (use ```java for Java code).
Use a professional yet encouraging tone, suitable for beginners and intermediate developers.
If the input code does not look like valid Java code or is empty, politely ask the user to provide valid Java code.
"""

EXPLAIN_PROMPT = """Explain the following Java code step-by-step.
Break it down into easy-to-understand logical blocks.
Explain the concepts used (e.g., loops, OOP concepts, data structures, recursion) and clarify what the overall code accomplishes.

Here is the Java code:
```java
{code}
```
"""

FIND_BUGS_PROMPT = """Analyze the following Java code for any bugs, logical errors, performance issues, or bad practices.
For each issue you find:
1. Explain the problem clearly (why it is a bug or issue).
2. Show where it occurs in the code.
3. Provide the corrected version of the code.
4. Explain how the correction fixes the problem.

If the code has no bugs, praise the user and suggest any minor improvements if applicable.

Here is the Java code:
```java
{code}
```
"""

OPTIMIZE_PROMPT = """Analyze the following Java code and suggest optimizations.
Focus on:
1. Time Complexity (e.g., replacing inefficient algorithms/data structures).
2. Space Complexity (e.g., reducing memory footprint, reusing objects).
3. Code Readability and Modern Java Features (e.g., using Streams, modern switch expressions, try-with-resources where applicable).

For each suggestion, provide:
- The reason for optimization.
- The optimized Java code.
- A brief explanation of the performance trade-offs.

Here is the Java code:
```java
{code}
```
"""

GENERATE_COMMENTS_PROMPT = """Add comprehensive and clean Javadoc comments for classes and methods, as well as clear inline comments for complex logic in the following Java code.
Ensure the comments follow Java documentation standards.
Do not modify the underlying code logic or rename variables, only add comments.
Return the complete, updated code.

Here is the Java code:
```java
{code}
```
"""

# Map task names to their respective prompts
PROMPT_TEMPLATES = {
    "Explain Code": EXPLAIN_PROMPT,
    "Find Bugs": FIND_BUGS_PROMPT,
    "Optimize Code": OPTIMIZE_PROMPT,
    "Generate Comments": GENERATE_COMMENTS_PROMPT
}
