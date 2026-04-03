"""CLI entry point for research-router.

Usage:
    python main.py ask <provider> "<prompt>" [--task <name>]
    python main.py compare <model1> <model2> ... "<prompt>" [--analyzer <model>] [--task <name>]
    python main.py review <executor> by <reviewer> "<prompt>" [--task <name>]
    python main.py synthesize [--analyzer <model>] [--task <name>]
    python main.py synthesize current
    python main.py task list
    python main.py task show [--task <name>]
    python main.py task use <name>
    python main.py task new <name>
"""

import argparse
import sys
import os

# Fix Windows console encoding for non-ASCII output
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from router import ask, compare, review, synthesize
from session import SessionManager
import config
import strategy


def main():
    current_task = SessionManager.get_current_task()

    parser = argparse.ArgumentParser(description="Research Router - Multi-model research assistant")
    subparsers = parser.add_subparsers(dest="command")

    # ask
    ask_parser = subparsers.add_parser("ask", help="Ask a single model")
    ask_parser.add_argument("provider", nargs="?", default=None,
                            help="Model provider (default: auto-select via strategy)")
    ask_parser.add_argument("prompt", help="Your question / prompt")
    ask_parser.add_argument("--task", default=current_task, help=f"Task name (current: '{current_task}')")

    # compare
    compare_parser = subparsers.add_parser("compare", help="Compare multiple models")
    compare_parser.add_argument("providers", nargs="+",
                                help="Model providers followed by prompt, last arg is the prompt")
    compare_parser.add_argument("--analyzer", default=config.get("default_analyzer", "qwen"),
                                help=f"Model for analysis summary (default: {config.get('default_analyzer', 'qwen')})")
    compare_parser.add_argument("--task", default=current_task, help=f"Task name (current: '{current_task}')")

    # review
    review_parser = subparsers.add_parser("review", help="Execute with one model, review with another")
    review_parser.add_argument("executor", nargs="?", default=None,
                               help="Executor model (default: auto-select)")
    review_parser.add_argument("reviewer", nargs="?", default=None,
                               help="Reviewer model (default: auto-select)")
    review_parser.add_argument("prompt", help="Your question / prompt")
    review_parser.add_argument("--task", default=current_task, help=f"Task name (current: '{current_task}')")

    # synthesize
    synth_parser = subparsers.add_parser("synthesize", help="Summarize current task history")
    synth_parser.add_argument("task_positional", nargs="?", default=None,
                              help="Task name or 'current' (default: current task)")
    synth_parser.add_argument("--analyzer", default=config.get("default_analyzer", "qwen"),
                              help=f"Model for synthesis (default: {config.get('default_analyzer', 'qwen')})")
    synth_parser.add_argument("--task", default=None, help="Task name")

    # export
    export_parser = subparsers.add_parser("export", help="Export task history to markdown")
    export_parser.add_argument("task_name", help="Task name to export")
    export_parser.add_argument("--output", "-o", default=None,
                               help="Output file path (default: exports/<task_name>.md)")

    # task
    task_parser = subparsers.add_parser("task", help="Session management")
    task_sub = task_parser.add_subparsers(dest="task_action")

    task_show = task_sub.add_parser("show", help="Show task content")
    task_show.add_argument("--task", default=current_task, help=f"Task name (current: '{current_task}')")

    task_list = task_sub.add_parser("list", help="List all tasks")

    task_new = task_sub.add_parser("new", help="Create a new task")
    task_new.add_argument("name", help="New task name")

    task_use = task_sub.add_parser("use", help="Set current task")
    task_use.add_argument("name", help="Task name to use")

    args = parser.parse_args()

    if args.command == "ask":
        provider = args.provider or strategy.get_default_ask_model(args.prompt)
        try:
            print(f"[{provider}] Thinking...\n")
            response = ask(provider, args.prompt, task_name=args.task)
            print(response)
            print(f"\n--- saved to session '{args.task}' ---")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "compare":
        if len(args.providers) < 1:
            print("Error: compare requires a prompt.", file=sys.stderr)
            sys.exit(1)
        # If only 1 arg, it's just the prompt — auto-select models
        if len(args.providers) == 1:
            prompt = args.providers[0]
            providers = strategy.get_default_compare_models(prompt)
        else:
            providers = args.providers[:-1]
            prompt = args.providers[-1]
        try:
            print(f"Comparing {', '.join(providers)} on: {prompt[:60]}...\n")
            results, analysis = compare(providers, prompt, analyzer=args.analyzer, task_name=args.task)

            print("=== RAW OUTPUT ===")
            for name, resp in results.items():
                print(f"[{name}]")
                print(resp)
                print()
            print("=== ANALYSIS ===")
            print(analysis)
            print(f"\n--- results saved to session '{args.task}' ---")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "review":
        executor = args.executor
        reviewer = args.reviewer
        if executor is None or reviewer is None:
            auto_exec, auto_rev = strategy.get_default_review_pair(args.prompt)
            executor = executor or auto_exec
            reviewer = reviewer or auto_rev
        try:
            print(f"[{executor}] Executing...\n")
            exec_resp, rev_resp = review(executor, reviewer, args.prompt, task_name=args.task)
            print("=== EXECUTOR OUTPUT ===")
            print(exec_resp)
            print("\n=== REVIEW ===")
            print(rev_resp)
            print(f"\n--- saved to session '{args.task}' ---")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "synthesize":
        # Resolve task name: --task > positional > current_task default
        if args.task:
            task = args.task
        elif args.task_positional and args.task_positional != "current":
            task = args.task_positional
        else:
            task = current_task
        try:
            print(f"[{args.analyzer}] Synthesizing session '{task}'...\n")
            response = synthesize(analyzer=args.analyzer, task_name=task)
            print("=== SYNTHESIZE ===")
            print(response)
            print(f"\n--- synthesis saved to session '{task}' ---")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "export":
        session = SessionManager(args.task_name)
        if not session.data["entries"]:
            print(f"No entries found in task '{args.task_name}'.", file=sys.stderr)
            sys.exit(1)
        md = session.export_markdown()
        # Determine output path
        if args.output:
            out_path = args.output
        else:
            exports_dir = os.path.join(os.path.dirname(__file__), "exports")
            os.makedirs(exports_dir, exist_ok=True)
            out_path = os.path.join(exports_dir, f"{args.task_name}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Exported {len(session.data['entries'])} entries to {out_path}")

    elif args.command == "task":
        if args.task_action == "show":
            session = SessionManager(args.task)
            print(session.show())
        elif args.task_action == "list":
            sessions = SessionManager.list_sessions()
            print(f"Available tasks (current is marked with *):")
            for s in sessions:
                star = "*" if s == current_task else " "
                print(f" {star} {s}")
        elif args.task_action == "new":
            session = SessionManager(args.name)
            session.save()
            SessionManager.set_current_task(args.name)
            print(f"Task '{args.name}' created and set as current.")
        elif args.task_action == "use":
            sessions = SessionManager.list_sessions()
            if args.name not in sessions:
                print(f"Error: Task '{args.name}' does not exist. Use 'task new {args.name}' first.")
                sys.exit(1)
            SessionManager.set_current_task(args.name)
            print(f"Switched to task '{args.name}'.")
        else:
            task_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
