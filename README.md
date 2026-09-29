# commit-it 🚀

`commit-it` is a lightweight, local CLI tool that reads your staged `git diff` and generates conventional commit messages using local LLMs via [Ollama](https://ollama.ai) (defaulting to `qwen2.5-coder`).

- **100% Local & Private**: No API keys, no network requests to third-party services.
- **Conventional Commits**: Produces clean, imperative commit messages with key structural bullet points.
- **Fast & Flexible**: Optimized for `qwen2.5-coder:14b` or `7b`, but works with any model loaded in Ollama.

---

## 📋 Requirements

- [Ollama](https://ollama.ai) running locally (`ollama serve`).
- A coding model pulled in Ollama:
  ```bash
  ollama pull qwen2.5-coder:14b-instruct-q4_K_S
  # or
  ollama pull qwen2.5-coder:7b
  ```

---

## ⚡ Quick Start

### Option A: Using Nix Flake + direnv (Recommended)

If you use `nix` and `direnv`, everything (Python 3.14 runtime, `uv`, and dependencies) is isolated automatically:

```bash
git clone https://github.com/your-username/commit-it.git
cd commit-it
direnv allow
```

### Option B: Without Nix (Standard Python / uv)

Requires Python 3.11+:

```bash
git clone https://github.com/your-username/commit-it.git
cd commit-it

# Using uv (fastest)
uv venv .venv
source .venv/bin/activate
uv pip install -e .

# Or using standard pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 💻 Standalone Usage

Stage your changes and run `commit-it`:

```bash
git add .
commit-it
```

### Options

Specify a different model:

```bash
commit-it -m qwen3.5:latest
```

**Expose as a native Git subcommand:**  
Once installed on your `$PATH`, running `git-commit-it` or setting up an alias allows you to invoke it directly via Git.

---

## 🛠️ Recommended Workflow: Global Git Alias

The best way to use `commit-it` across all your projects is to set up a global Git alias. This allows you to generate a message, review it, and commit with a single interactive prompt.

Add the alias to your global `~/.gitconfig`:

```ini
[alias]
    ai-commit = "!f() { msg=$(commit-it \"$@\") && echo -e \"\\n$msg\\n\" && read -p \"Commit with this message? [y/N] \" confirm && [[ $confirm == [yY]* ]] && git commit -m \"$msg\"; }; f"
```

Or set it via terminal:

```bash
git config --global alias.ai-commit '!f() { msg=$(commit-it "$@") && echo -e "\n$msg\n" && read -p "Commit with this message? [y/N] " confirm && [[ $confirm == [yY]* ]] && git commit -m "$msg"; }; f'
```

### Daily Usage with Alias

```bash
# 1. Stage changes in any repository
git add .

# 2. Run your new alias
git ai-commit

# 3. Pass custom model flags if needed
git ai-commit -m qwen3.5:9b
```

---

## 📄 License

MIT