"""Generate docs/data.json from Harbor benchmark results."""

import json
import statistics
from analyze import parse_job, ORACLE_JOB, COMPOSER2_JOB


def main():
    oracle = parse_job(ORACLE_JOB)
    composer2 = parse_job(COMPOSER2_JOB)

    all_tasks = sorted(set(oracle.keys()) | set(composer2.keys()))

    # Per-task results
    tasks = []
    for task in all_tasks:
        o = oracle.get(task, {})
        c = composer2.get(task, {})
        exc = c.get("exception")

        if exc:
            status = "error"
            c_reward = None
        elif c.get("reward") == 1.0:
            status = "pass"
            c_reward = 1.0
        elif c.get("reward") == 0.0:
            status = "fail"
            c_reward = 0.0
        elif c.get("reward") is not None:
            status = "partial"
            c_reward = c["reward"]
        else:
            status = "unknown"
            c_reward = None

        note = ""
        if o.get("reward") is not None and c_reward is not None:
            if o["reward"] == 0.0 and c_reward > 0:
                note = "Agent solved (no oracle)"
            elif o["reward"] == 1.0 and c_reward == 0.0:
                note = "Regression"

        tasks.append({
            "name": task,
            "composer2": c_reward,
            "oracle": o.get("reward"),
            "status": status,
            "note": note,
            "exec_time_secs": round(c.get("agent_exec_secs") or 0, 1),
            "error_type": exc.get("exception_type") if exc else None,
        })

    # Summary stats
    scored = [t for t in tasks if t["composer2"] is not None]
    rewards = [t["composer2"] for t in scored]

    exec_times = sorted([t["exec_time_secs"] for t in scored if t["exec_time_secs"] > 0])

    summary = {
        "model": "Cursor Composer 2",
        "dataset": "OpenThoughts-TBLite",
        "framework": "Harbor v0.1.45",
        "total_tasks": 100,
        "scored": len(scored),
        "errors": sum(1 for t in tasks if t["status"] == "error"),
        "mean_reward": round(statistics.mean(rewards), 4),
        "median_reward": round(statistics.median(rewards), 4),
        "std_dev": round(statistics.stdev(rewards), 4),
        "perfect": sum(1 for r in rewards if r == 1.0),
        "partial": sum(1 for r in rewards if 0 < r < 1),
        "zero": sum(1 for r in rewards if r == 0.0),
        "pass_rate": round(100 * sum(1 for r in rewards if r > 0) / len(rewards), 1),
        "agent_solved_count": sum(1 for t in tasks if t["note"] == "Agent solved (no oracle)"),
        "regression_count": sum(1 for t in tasks if t["note"] == "Regression"),
        "timing": {
            "min": exec_times[0] if exec_times else 0,
            "p50": exec_times[len(exec_times) // 2] if exec_times else 0,
            "p90": exec_times[int(len(exec_times) * 0.9)] if exec_times else 0,
            "p95": exec_times[int(len(exec_times) * 0.95)] if exec_times else 0,
            "max": exec_times[-1] if exec_times else 0,
            "mean": round(statistics.mean(exec_times), 1) if exec_times else 0,
        },
    }

    # Published leaderboard (from OpenThoughts-TBLite GitHub/blog)
    leaderboard = [
        {"model": "Cursor Composer 2", "tblite": 80.1, "tb2": 61.7, "ours": True, "note": "cursor-cli agent"},
        {"model": "Kimi-K2.5", "tblite": 75.1, "tb2": 35.2, "ours": False, "note": "terminus-2 agent"},
        {"model": "GLM-4.7", "tblite": 67.7, "tb2": 35.2, "ours": False, "note": "terminus-2 agent"},
        {"model": "Claude Haiku 4.5", "tblite": 64.4, "tb2": 28.3, "ours": False, "note": "terminus-2 agent"},
        {"model": "GPT-5-mini", "tblite": 50.5, "tb2": 24.9, "ours": False, "note": "terminus-2 agent"},
        {"model": "Qwen3-Coder-480B", "tblite": 42.1, "tb2": 26.6, "ours": False, "note": "terminus-2 agent"},
        {"model": "Qwen3-235B", "tblite": 37.0, "tb2": 14.6, "ours": False, "note": "terminus-2 agent"},
        {"model": "Nemotron-3-Nano-30B", "tblite": 21.5, "tb2": 9.5, "ours": False, "note": "terminus-2 agent"},
    ]

    data = {
        "summary": summary,
        "leaderboard": leaderboard,
        "tasks": tasks,
    }

    with open("docs/data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Written docs/data.json ({len(tasks)} tasks, {len(leaderboard)} leaderboard entries)")


if __name__ == "__main__":
    main()
