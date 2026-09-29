import asyncio
import argparse
import sys
import httpx
from rich.console import Console

console = Console()

DEFAULT_MODEL = "qwen2.5-coder:14b-instruct-q4_K_S"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are an expert software developer writing a git commit message.
Analyze the provided `git diff --cached` output and summarize the changes.

Rules:
1. Follow the Conventional Commits specification (e.g., feat, fix, docs, refactor, chore, test).
2. The summary line MUST be concise (under 72 characters) and written in imperative mood.
3. Provide a bulleted list explaining key changes if necessary.
4. Output ONLY the raw commit message. Do NOT use markdown code blocks or intro/outro prose.
"""

async def get_staged_diff() -> str:
    proc = await asyncio.create_subprocess_exec(
        "git", "diff", "--cached",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Git command failed: {stderr.decode().strip()}")
    return stdout.decode("utf-8").strip()

async def generate_commit_message(diff: str, model: str) -> str:
    prompt = f"System:\n{SYSTEM_PROMPT}\n\nDiff:\n{diff}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                    }
                },
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except httpx.ConnectError:
            raise RuntimeError(
                "Could not connect to Ollama. Ensure Ollama is running (`ollama serve`)."
            )

async def run() -> None:
    parser = argparse.ArgumentParser(description="Generate commit message using Ollama.")
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})"
    )
    args = parser.parse_args()

    try:
        diff = await get_staged_diff()
        if not diff:
            console.print("[yellow]No staged changes detected. Stage files using `git add` first.[/yellow]")
            sys.exit(0)

        with console.status(f"[bold green]Generating commit message via {args.model}...[/bold green]"):
            message = await generate_commit_message(diff, args.model)

        console.print("\n[bold cyan]Suggested Commit Message:[/bold cyan]\n")
        console.print(f"[bold white]{message}[/bold white]\n")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()
