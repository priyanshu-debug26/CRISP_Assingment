import datetime

def generate_report(results: list, file_path: str, model_name: str, mode: str):
    """
    Compiles prompt execution results list into a beautifully formatted Markdown report.
    
    Parameters:
        results (list): List of dicts containing prompt details and LLM outputs.
        file_path (str): Output destination path.
        model_name (str): The name of the model used during execution.
        mode (str): Mode of execution ('Live' or 'Mock').
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(file_path, "w", encoding="utf-8") as f:
        # Header
        f.write("# Prompt Engineering Mastery Results\n\n")
        f.write("This report compiles the outputs and educational observations for 20 prompting examples across four core categories.\n\n")
        f.write("## Execution Metadata\n\n")
        f.write(f"- **Timestamp**: {now}\n")
        f.write(f"- **Execution Mode**: {mode}\n")
        f.write(f"- **Model**: `{model_name}`\n\n")
        
        # Summary Table
        f.write("## Summary Table\n\n")
        f.write("| ID | Technique | Domain | Status |\n")
        f.write("|---|---|---|---|\n")
        for res in results:
            status = "✅ Completed" if "Error" not in res["response"] else "⚠️ API Error / Fallback"
            f.write(f"| `{res['id']}` | {res['category']} | {res['domain']} | {status} |\n")
        f.write("\n---\n\n")
        
        # Detailed results section
        f.write("## Detailed Prompts & Outputs\n\n")
        
        current_category = None
        for res in results:
            # Add header for new category
            if res["category"] != current_category:
                current_category = res["category"]
                f.write(f"### 📁 Category: {current_category}\n\n")
                
            f.write(f"#### 🔍 Prompt: `{res['id']}` ({res['domain']})\n\n")
            f.write("**Description**:\n")
            f.write(f"{res['description']}\n\n")
            
            f.write("**System/Human Prompt Input**:\n")
            f.write("```text\n")
            f.write(f"{res['prompt']}\n")
            f.write("```\n\n")
            
            f.write("**Model Response**:\n")
            # If the response contains markdown codeblocks, we wrap it cleanly
            response_clean = res["response"].strip()
            f.write(f"{response_clean}\n\n")
            
            f.write("> **Educational Observation**:\n")
            f.write(f"> {res['observation']}\n\n")
            f.write("---\n\n")
            
        # Footer
        f.write("\n*Report generated automatically by the Prompt Engineering CLI workshop tool.*\n")
