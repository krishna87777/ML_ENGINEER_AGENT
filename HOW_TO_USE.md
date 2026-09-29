# How to use `ML_ENGINEER_AGENT.md`

This guide takes you from an empty folder to a finished `REPORT.md`, in plain steps.

---

## What you need

- A coding agent that can run shell commands in a folder, such as Claude Code, Cursor, Aider or Codex CLI.
- Python, plus whatever ML libraries your task needs.
- Your data.
- Optional: `git`. The agent commits after every experiment if the folder is a git repo.

---

## Step 1: Set up the folder

```
my-task/
├── ML_ENGINEER_AGENT.md      ← copy this file here
└── input/                    ← put your data here (CSV, images, JSON, ...)
```

```bash
mkdir my-task && cd my-task
cp /path/to/ML_ENGINEER_AGENT.md .
mkdir input && cp -r /path/to/your/data/* input/
git init && git add . && git commit -m "start"     # optional but recommended
```

## Step 2: Start the agent

Open your coding agent in `my-task/` and send it one message:

> **Read ML_ENGINEER_AGENT.md and follow it exactly.**

## Step 3: Answer the 5 setup questions

The agent will **stop and ask** these before writing any code. Answer them honestly, because everything else depends on them.

| # | Question | Example answer |
|---|---|---|
| 1 | **What hardware?** (most important) | "RTX 4050 laptop, 6 GB VRAM, 16 GB RAM" or "CPU only, 12 threads" |
| 2 | **Goal and metric**, and is higher or lower better? | "Predict churn. Metric: ROC-AUC, higher is better" |
| 3 | **Where is the data?** | "`./input`" (the default) |
| 4 | **Time per experiment** | "5 minutes" (the default) |
| 5 | **Total budget** | "30 experiments" or "4 hours" (default: 20 steps) |

Tips for good answers:
- **Give an exact metric.** "Make it better" is not a metric. "Word accuracy on the dev split ≥ 0.95" is.
- **State hard limits up front**, e.g. "must stay under 8 GB VRAM" or "must run in < 2 s/page on CPU".
- **Say what must not change**, e.g. "output must be identical to the baseline".

## Step 4: Let it run, and don't interrupt

After you confirm the setup, the agent loops on its own and will **not** ask "should I continue?".
While it runs, you can watch the lab notebook grow:

```bash
column -t -s $'\t' working/journal.tsv | less -S       # pretty-print the journal
grep -c . working/journal.tsv                         # how many experiments so far
```

Each row has the experiment `id`, its `parent` (which experiment it grew from), `stage` (draft / improve / debug),
`status` (good / buggy / crash), the `metric`, the time, the VRAM, **what it tried**, and **what actually happened**.

## Step 5: Read the results

When the budget runs out you get:

| File | What it is |
|---|---|
| `working/best_solution.py` | the winning experiment; run it to reproduce the best score |
| `working/REPORT.md` | Introduction · Preprocessing · Methods · Results · Future work, **only real numbers from the journal** |
| `working/journal.tsv` | every experiment, including the failures |
| `working/sol_<id>.py`, `run_<id>.log` | each experiment's code and log |
| `working/submission.csv` | predictions on the test data, if test data exists |

The final summary also prints the best score, **its lineage** (draft → the improvements that were kept), and the **top 3 things that did not work**.

---

## Checking the result (please don't skip this)

The agent optimises exactly what you measure, so a good score can still be wrong. Before you trust the winner:

1. **Keep a sealed test set** the search never sees, and score the final solution on it **once**.
2. **Try it on truly new data**: a new photo, a new document type, a new user. A preset tuned on one image can score 0.98 there and 0.36 on the next.
3. **Split by source**, e.g. by writer, question or document, not by row, so near-copies don't sit on both sides.
4. **Read 10–20 real outputs by eye.** Metrics missed the biggest bugs in these projects; reading outputs caught them.
5. **Check that the scorer itself is right.** Twice, a broken reference made real improvements look like failures.
6. **Re-run the winner with 2–3 random seeds** if its lead is small.

---

## Adapting the file to your project

`ML_ENGINEER_AGENT.md` is plain text, so edit it freely:

- **Big training runs?** Raise the per-experiment time budget (e.g. 30 min or 2 h) and lower the total step count.
- **Hard targets?** Write them into your answer to question 2 as a list (T1, T2, …), and ask for the metric
  `min(value / target)` so ≥ 1.0 means every target passes.
- **Speed work?** Add a quality gate, e.g. "an experiment only counts as good if output quality ≥ 0.995 of the baseline".
- **Shared GPU?** Tell the agent the VRAM cap, and ask it to wrap every run in a guard that kills its own process if it goes over.

---

## Common problems

| Problem | Fix |
|---|---|
| Agent asks "should I continue?" | Reply: "Follow the file: do not ask, continue until the budget is used." |
| Out of memory (OOM) | That's expected, and the file treats it as a bug: batch size → model size → method. Check your hardware answer was right |
| Agent reads whole training logs | Remind it: "Context hygiene: redirect to a log, grep the metric, `tail -n 50` only on failure." |
| Agent changes several things at once | Remind it: "IMPROVE = exactly ONE atomic change off the best node." |
| Scores jump around between identical runs | Fix the random seed, or average 3 runs before comparing |
| Context lost mid-run | Ask it to "recover state from `journal.tsv`". Everything it needs is in there |
