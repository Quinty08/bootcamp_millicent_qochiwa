\# Orchestration Plan — Homework 15



\## Overview

This plan maps the project to a simple pipeline (DAG), lists tasks with inputs/outputs, and specifies logging, checkpoints, retry policy and which parts to automate now vs later. The project implements a simple linear forecasting/modeling flow and serves predictions via an API. This plan is intentionally small and idempotent.



---



\## 1) Tasks (decomposition)



| # | Task name           | Inputs                         | Outputs                         | Idempotent? | Checkpoint artifact      | Log location          |

|---|---------------------|--------------------------------|----------------------------------|-------------:|-------------------------|-----------------------|

| 1 | ingest/generate     | external API or generator code | data/raw\_prices.csv              | Yes (Y)     | data/raw\_prices.csv      | logs/ingest.log       |

| 2 | validate            | data/raw\_prices.csv            | data/validated\_prices.csv        | Yes (Y)     | data/validated\_prices.csv| logs/validate.log     |

| 3 | clean \& transform   | data/validated\_prices.csv      | data/prices\_clean.csv            | Yes (Y)     | data/prices\_clean.csv    | logs/clean.log        |

| 4 | feature\_engineer    | data/prices\_clean.csv          | data/features.csv                | Yes (Y)     | data/features.csv        | logs/feat\_eng.log     |

| 5 | train\_or\_score      | data/features.csv              | model/model\_v{ts}.pkl or scores  | Yes (Y)     | model/model\_v{ts}.pkl    | logs/train.log        |

| 6 | evaluate/report     | model/model\_v{ts}.pkl, data    | reports/report\_{ts}.pdf or txt   | Yes (Y)     | reports/report\_{ts}.pdf  | logs/report.log       |

| 7 | serve/deploy (API)  | model/model\_active.pkl         | running API endpoints            | N (service) | model/model\_active.pkl   | logs/api.log          |



Notes:

\- `{ts}` indicates a timestamp or version to preserve checkpoints.

\- All file outputs are placed under project `data/`, `model/`, `reports/` folders.



---



\## 2) DAG (dependencies)

Simple ASCII DAG (top → bottom):



ingest/generate

↓

validate

↓

clean \& transform

↓

feature\_engineer

↓

train\_or\_score

↓

evaluate/report

↓

serve/deploy (optional / separate process







Parallelizable steps:

\- `evaluate/report` can run in parallel for different test sets.

\- `serve` runs independently once `model\_active` is updated.



---



\## 3) Logging \& Checkpoint strategy

\*\*Logging:\*\*

\- Use Python `logging` (INFO+). Each task writes a rotating log file `logs/{task}.log` and stdout.

\- Log messages: start/end timestamps, elapsed time, rows in/out, key parameter values, exceptions with stack traces.



\*\*Checkpoints:\*\*

\- After each task write a checkpoint artifact (file paths above). Use deterministic naming or versioned names (`model\_vYYYYMMDD\_HHMM.pkl`) and keep a `model/registry.json` linking `active` model.

\- Checkpointing reduces recomputation and allows partial reruns.



\*\*Where to store:\*\* All artifacts are local project folders (data/, model/, reports/). In production store in object storage (S3) with the same naming scheme.



---



\## 4) Failure points \& retry policy

\- \*\*Ingest failures (network/API)\*\*: retry up to 3 times with exponential backoff (0.5s → 1s → 2s). If still failing, create an incident and stop pipeline.

\- \*\*Validation errors (schema mismatch)\*\*: fail fast, write detailed schema diff to `logs/validate.log`, alert data owner.

\- \*\*Cleaning/feature errors\*\*: log error, checkpoint last good artifact, stop and notify.

\- \*\*Training divergence\*\*: if evaluation metric degrades >10% vs baseline, do not mark model active; notify ML owner.

\- \*\*API system issues\*\*: platform on-call handles p95/p99 latency or high error rates.



---



\## 5) Automation decisions (what to automate now vs later)

\*\*Automate now (high value, low risk):\*\*

\- Ingest (scheduled), validate, clean, feature generation, model training pipeline (run nightly or on-demand).

\- Checkpointing and logs automatically produced.



\*\*Keep manual initially:\*\*

\- Report finalization for stakeholders (formatting + narrative) — requires human judgment.

\- Production promotion of a model (manual sign-off after automatic evaluation) — safer for handoff.



Rationale: automate repetitive deterministic steps to reduce manual errors and save time; keep judgement-heavy steps manual until metrics and reviews are stable.



---



\## 6) Operational runbook (short)

\- On data freshness alert: verify `data/raw\_prices.csv` timestamp, confirm upstream API status.

\- On schema mismatch: run `python scripts/validate\_schema.py --input data/raw\_prices.csv` and open `logs/validate.log`.

\- For model rollback: replace `model/model\_active.pkl` with previous `model/model\_v{prev}.pkl` and restart API service; notify stakeholders.



---



