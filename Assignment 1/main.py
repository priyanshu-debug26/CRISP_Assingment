import os
import argparse
import sys

# Import Rich elements
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.text import Text

# Local imports
from api_helper import GroqAPIHelper
from prompts import PROMPTS
from markdown_generator import generate_report

# Initialize Rich console
console = Console()

def print_banner(mode: str, model_name: str):
    """
    Renders a polished, professional ASCII banner for the CLI interface.
    """
    banner_text = Text()
    banner_text.append("\n ╔══════════════════════════════════════════════════════════════════════╗\n", style="bold double blue")
    banner_text.append(" ║", style="bold double blue")
    banner_text.append("                 PROMPT ENGINEERING MASTERY WORKSHOP                  ", style="bold cyan")
    banner_text.append("║\n", style="bold double blue")
    banner_text.append(" ╚══════════════════════════════════════════════════════════════════════╝\n", style="bold double blue")
    
    console.print(Align.center(banner_text))
    
    # Metadata details panel
    metadata_table = Table.grid(padding=1)
    metadata_table.add_column(style="bold yellow", justify="right")
    metadata_table.add_column(style="white", justify="left")
    
    metadata_table.add_row("Execution Mode : ", mode)
    metadata_table.add_row("Target LLM Model: ", f"`{model_name}`")
    
    metadata_panel = Panel(
        Align.center(metadata_table),
        title="[bold green]System Configurations[/bold green]",
        border_style="blue",
        expand=False
    )
    console.print(Align.center(metadata_panel))
    console.print("\n")


def parse_arguments():
    """
    Sets up the CLI command line flags.
    """
    parser = argparse.ArgumentParser(
        description="Prompt Engineering Mastery Workshop CLI tool. Runs 20 prompts across 4 core techniques."
    )
    
    # Exclusive group to force execution mode
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--live",
        action="store_true",
        help="Force execution through the live Groq API (requires valid API key)."
    )
    group.add_argument(
        "--mock",
        action="store_true",
        help="Force execution in offline Mock Mode using high-fidelity pre-compiled responses."
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specify a custom Groq model (e.g. llama-3.3-70b-specdec, mixtral-8x7b-32768)."
    )
    
    return parser.parse_args()


def run_workbench():
    """
    Orchestrates execution: parses flags, launches prompts, prints consoles,
    and saves markdown report outcomes.
    """
    args = parse_arguments()
    
    # 1. Resolve Execution Mode and API configuration
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    
    # Determine mode string
    if args.live:
        mode = "FORCED LIVE MODE"
        use_live = True
    elif args.mock:
        mode = "FORCED MOCK MODE"
        use_live = False
    else:
        # Auto Mode
        if api_key:
            mode = "AUTO MODE (LIVE API)"
            use_live = True
        else:
            mode = "AUTO MODE (MOCK FALLBACK - NO API KEY DETECTED)"
            use_live = False
            
    # Resolve Model name
    model_name = args.model or os.getenv("GROQ_DEFAULT_MODEL", "llama-3.1-8b-instant")
    
    # 2. Print dashboard banner
    print_banner(mode, model_name)
    
    # 3. Initialize API Helper
    try:
        api = GroqAPIHelper(use_live=use_live, model_name=model_name, api_key=api_key)
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] Failed to load configuration client: {str(e)}")
        sys.exit(1)
        
    # Re-verify live status (in case initialization auto-toggled off due to missing libraries or keys)
    actual_mode = "Live API Mode" if api.is_live else "Offline Mock Mode"
    if use_live and not api.is_live:
        console.print("[bold yellow]⚠️ Warning: Forced Live Mode requested, but GROQ_API_KEY is missing or invalid. Falling back to Mock Mode.[/bold yellow]\n")
        actual_mode = "Offline Mock Mode (Fallback)"

    # 4. Prompt Execution Loop
    results = []
    
    console.print("[bold cyan]🔄 Running Prompt Engineering Suite (20 prompts)...[/bold cyan]\n")
    
    # Rich Progress Bar Spinner
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[yellow]Processing...", total=len(PROMPTS))
        
        for idx, p_item in enumerate(PROMPTS):
            p_id = p_item["id"]
            category = p_item["category"]
            domain = p_item["domain"]
            prompt_text = p_item["prompt"]
            desc = p_item["description"]
            obs = p_item["observation"]
            
            progress.update(task, description=f"[yellow]Executing {category} -> {domain} ({idx+1}/20)...[/yellow]")
            
            # Fetch model response (either live or mock)
            response = api.get_response(p_id, prompt_text)
            
            results.append({
                "id": p_id,
                "category": category,
                "domain": domain,
                "description": desc,
                "prompt": prompt_text,
                "response": response,
                "observation": obs
            })
            
            progress.advance(task)
            
    console.print("\n[bold green]✅ All 20 prompts executed successfully![/bold green]\n")
    
    # 5. Display Summary Grid
    summary_table = Table(
        title="[bold green]Prompts Execution Summary[/bold green]",
        border_style="blue",
        header_style="bold cyan"
    )
    summary_table.add_column("ID", style="yellow")
    summary_table.add_column("Category", style="magenta")
    summary_table.add_column("Sub-Domain", style="green")
    summary_table.add_column("Status", justify="center")
    
    for res in results:
        status_symbol = "✅ Complete" if "Error" not in res["response"] else "⚠️ Fallback"
        summary_table.add_row(res["id"], res["category"], res["domain"], status_symbol)
        
    console.print(summary_table)
    console.print("\n")
    
    # 6. Display a couple of detailed response panels for preview
    console.print("[bold cyan]👁️ Previewing selected technique outputs in terminal:[/bold cyan]\n")
    
    # Choose 2 diverse previews (e.g. CoT Math and Role Engineer)
    previews = ["cot_math", "role_engineer"]
    for p_id in previews:
        res = next((item for item in results if item["id"] == p_id), None)
        if res:
            preview_content = Text()
            preview_content.append(f"Prompt:\n", style="bold yellow")
            preview_content.append(f"{res['prompt']}\n\n", style="italic white")
            preview_content.append(f"Response:\n", style="bold green")
            preview_content.append(f"{res['response']}\n\n", style="white")
            preview_content.append(f"Tutor Observation:\n", style="bold magenta")
            preview_content.append(f"{res['observation']}", style="italic white")
            
            panel = Panel(
                preview_content,
                title=f"[bold cyan]{res['category']} ({res['domain']})[/bold cyan]",
                border_style="blue",
                padding=(1, 2)
            )
            console.print(panel)
            console.print("\n")
            
    # 7. Write Markdown Report
    report_file = "prompt_engineering_results.md"
    try:
        generate_report(results, report_file, model_name, actual_mode)
        console.print(f"[bold green]💾 Markdown report generated automatically:[/bold green] [bold white]{report_file}[/bold white]")
        console.print("Evaluate this file to review complete prompts and outputs.\n")
    except Exception as e:
        console.print(f"[bold red]Error saving Markdown report:[/bold red] {str(e)}\n")


if __name__ == "__main__":
    try:
        run_workbench()
    except KeyboardInterrupt:
        console.print("\n[bold red]✖ Process interrupted by user. Exiting...[/bold red]")
        sys.exit(0)
