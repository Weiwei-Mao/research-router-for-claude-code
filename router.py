"""Simple router: dispatches prompts to providers and logs to session."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from provider import get_provider
from session import SessionManager


def ask(provider_name: str, prompt: str, task_name: str = "default") -> str:
    """Call a single provider and save to session."""
    provider = get_provider(provider_name)
    response = provider.ask(prompt)
    session = SessionManager(task_name)
    session.add_entry(provider_name, prompt, response, kind="ask")
    return response


def _call_provider(name: str, prompt: str) -> tuple[str, str]:
    """Call a single provider, return (name, response)."""
    provider = get_provider(name)
    return name, provider.ask(prompt)


def compare(provider_names: list[str], prompt: str, analyzer: str = "gemini", task_name: str = "default") -> tuple[dict[str, str], str]:
    """Call multiple providers in parallel, then analyze with a designated model."""
    results = {}
    session = SessionManager(task_name)

    with ThreadPoolExecutor(max_workers=len(provider_names)) as pool:
        futures = {pool.submit(_call_provider, name, prompt): name for name in provider_names}
        for future in as_completed(futures):
            name, response = future.result()
            results[name] = response
            session.add_entry(name, prompt, response, kind="compare")

    # Build analysis prompt from raw outputs (truncate long responses)
    MAX_RESPONSE_LEN = 4000
    raw_section = "\n\n".join(
        f"[{name}]\n{resp[:MAX_RESPONSE_LEN]}{'...(truncated)' if len(resp) > MAX_RESPONSE_LEN else ''}"
        for name, resp in results.items()
    )
    analysis_prompt = (
        "You are a senior researcher. Multiple AI models answered the same question. "
        "Analyze their responses.\n\n"
        f"Question: {prompt}\n\n"
        f"{raw_section}\n\n"
        "Please provide:\n"
        "1. Consensus points (一致点)\n"
        "2. Disagreements (分歧点)\n"
        "3. Risks or concerns (风险点)\n"
        "4. Recommended approach (建议采用哪个思路)"
    )
    analysis_provider = get_provider(analyzer)
    analysis = analysis_provider.ask(analysis_prompt)
    session.add_entry(analyzer, analysis_prompt, analysis, kind="compare-analysis")

    return results, analysis


def review(executor_name: str, reviewer_name: str, prompt: str, task_name: str = "default") -> tuple[str, str]:
    """Execute with one model, review with another."""
    executor = get_provider(executor_name)
    executor_response = executor.ask(prompt)
    session = SessionManager(task_name)
    session.add_entry(executor_name, prompt, executor_response, kind="execute")

    review_prompt = (
        "You are a rigorous code and research reviewer. "
        "A model produced the following response to a user prompt. "
        "Please review it carefully.\n\n"
        f"Original prompt:\n{prompt}\n\n"
        f"Model response:\n{executor_response}\n\n"
        "Provide a structured review with these sections:\n"
        "1. Correct points (正确点) — what the response got right\n"
        "2. Potential issues (潜在问题) — anything incomplete, inaccurate, or misleading\n"
        "3. Risks (风险点) — bugs, edge cases, or assumptions that could fail\n"
        "4. Suggestions (修改建议) — concrete improvements or corrections"
    )
    reviewer = get_provider(reviewer_name)
    reviewer_response = reviewer.ask(review_prompt)
    session.add_entry(reviewer_name, review_prompt, reviewer_response, kind="review")
    return executor_response, reviewer_response


def synthesize(analyzer: str = "qwen", task_name: str = "default") -> str:
    """Summarize the entire session history with structured synthesis."""
    session = SessionManager(task_name)
    history = session.get_history_text()
    if not history:
        return "No history found for synthesis."

    synth_prompt = (
        "You are a senior researcher. Below is the full history of a research session "
        "involving multiple AI models (ask, compare, review interactions).\n\n"
        f"{history}\n\n"
        "Please provide a structured synthesis with these sections:\n\n"
        "1. Background summary (当前问题背景总结)\n"
        "   - What problem or question is being investigated?\n\n"
        "2. Approaches attempted (已尝试的方案/思路)\n"
        "   - What methods, models, or ideas have been explored?\n\n"
        "3. Key disagreements across models (各模型的主要分歧点)\n"
        "   - Where do models disagree or offer different perspectives?\n\n"
        "4. Confirmed reliable conclusions (已确认的可靠结论)\n"
        "   - What findings are consistently supported across models?\n\n"
        "5. Remaining uncertainties (仍存在的不确定性)\n"
        "   - What is still unclear, untested, or controversial?\n\n"
        "6. Recommended next steps (下一步建议)\n"
        "   - Concrete, research-oriented actions to take next."
    )
    provider = get_provider(analyzer)
    response = provider.ask(synth_prompt)
    session.add_entry(analyzer, synth_prompt, response, kind="synthesize")
    return response
