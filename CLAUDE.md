# auselectricity

Guide for Claude (interactive sessions and the factory workflow).

## Stack
Python backend (`backend/`, AEMO/NEMWeb/OpenNEM collectors, SQLite) + React (CRA) frontend in `frontend/`.

## Before you change things, read
- README.md
- DEVELOPER_GUIDE.md
- API_REFERENCE.md
- TECHNICAL_DOCUMENTATION.md

## Protected code (already in place - follow it)
This repo uses the `protect-working-code` rule: files listed in `docs/WORKING_SURFACES.md` are certified.
- Don't change their behaviour without the breaking-change checklist in that file.
- The pre-commit hook isn't installed in CI, so run the certified check yourself before every commit.
- Never set `CERTIFIED_OVERRIDE`. If a certified file must change, stop at the spec stage and ask the owner.

## Sensitive areas
`electricity_data.db` and the collection scripts - never rewrite or truncate stored data. Root `test_*.py` files hit live APIs; don't run them in bulk in CI.

## Notes
There is no root package.json, so run the certified-surfaces checker with node directly.

## Commands
```sh
# install
pip install -r requirements.txt && (cd frontend && npm install)
# checks (run all before every PR)
python -m compileall -q backend *.py
(cd frontend && npm run build)
node scripts/check-certified-surfaces.js
# run
python start_backend.py  and  (cd frontend && npm start)  # see QUICK_START.md
```

## Factory
Issues labelled `factory` run through `.claude/factory/BLUEPRINT.md` (triage -> spec -> implement -> verify -> merge risk -> PR).
Skills: `.claude/skills/factory-triage`, `verify-with-proof`, `merge-risk`. Use them in interactive sessions too.

## Verification gotchas
<!-- Append one line per lesson learned while verifying (ports, env vars, logins, flaky selectors). -->
