# HealthyLA — Project Instructions

## Activity Log (REQUIRED)

Every Claude session working in this repo MUST log activity to `output/data/activity.jsonl`.

**When to log:** After completing any meaningful step — finishing a file, processing data, hitting a blocker, making a key decision, starting a new task.

**How to log:** Append a single line to `output/data/activity.jsonl`. Each line is a self-contained JSON object:

```
{"timestamp":"2026-04-04T16:49:00","message":"DONE: Built landing page HTML"}
```

**Format rules:**
- One JSON object per line, no trailing comma, no wrapping array
- Use ISO 8601 timestamps
- Prefix the message with a status: `DONE:`, `TODO:`, `BLOCKED:`, `START:`, `NOTE:`
- Keep messages concise — under 120 characters
- **Append only** — never rewrite or truncate the file. Use a single shell append:
  ```
  echo '{"timestamp":"...","message":"..."}' >> output/data/activity.jsonl
  ```

This file is read by the ops dashboard and is how I track progress across multiple concurrent sessions.

## Project Context

This is a simple product that sends LA County restaurant health violation data to pest control and commercial cleaning companies. See PROMPT.md for the full build spec.

## Tech Constraints

- No databases, no backend servers, no auth, no frameworks (React, Next.js, etc.)
- Python 3 for scraping/data processing
- Plain HTML/CSS for web pages (Tailwind via CDN is fine)
- All output goes in `output/`
