"""Strategy system: auto-select default models based on command type and prompt content."""

CODE_KEYWORDS = {"code", "python", "bug", "error", "script", "function", "debug",
                 "implement", "fix", "simulation", "refactor", "compile", "runtime"}
RESEARCH_KEYWORDS = {"model", "research", "analysis", "hypothesis", "experiment",
                     "methodology", "compare", "evaluate", "theory"}

# --- provider name constants ---
CODEX = "codex"
GEMINI = "gemini"
QWEN = "qwen"


def _has_keywords(text: str, keywords: set[str]) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in keywords)


def _is_code_related(prompt: str) -> bool:
    return _has_keywords(prompt, CODE_KEYWORDS)


def _is_research_related(prompt: str) -> bool:
    return _has_keywords(prompt, RESEARCH_KEYWORDS)


# --- public API ---

def get_default_ask_model(prompt: str) -> str:
    """Default: qwen. Use gemini for research-oriented prompts."""
    if _is_research_related(prompt):
        return GEMINI
    return QWEN


def get_default_compare_models(prompt: str) -> list[str]:
    """Default: [gemini, qwen]. Add codex if code-related."""
    models = [GEMINI, QWEN]
    if _is_code_related(prompt):
        models.insert(0, CODEX)
    return models


def get_default_review_pair(prompt: str) -> tuple[str, str]:
    """Return (executor, reviewer).

    Code-related: codex executes, qwen reviews.
    Otherwise: qwen executes, gemini reviews.
    """
    if _is_code_related(prompt):
        return CODEX, QWEN
    return QWEN, GEMINI


def get_default_analyzer() -> str:
    """Default analyzer for compare-analysis and synthesize."""
    return QWEN
