# OpenClaw AgentHLE Auto Pipeline Repo

This repo packages the current OpenClaw profile + AgentHLE SOP + prompt hygiene checks into a portable seed repo for scaling benchmark task generation to other domains on another OpenClaw instance.

## Included
- `openclaw_profile/`: SOUL, AGENTS, USER, TOOLS, IDENTITY, MEMORY
- `docs/`: task acquisition SOP and prompt-generation SOPs
- `scripts/`: export/bundle helper scripts
- `reports/`: prompt leak scan outputs and latest 50-task audit

## Intended use
1. Copy the `openclaw_profile/` files into another OpenClaw workspace as a starting persona/configuration.
2. Read `docs/agenthle_task_acquisition_sop_draft.md` first.
3. Use `docs/gpt5pro_prompt_sop_for_domain_packs.md` to generate new-domain packs.
4. Run prompt leak checks before packaging public tasks.
5. Export handoff bundles using the helper scripts or adapted versions of them.

## Critical rules
- Public task prompts must not leak tutorial names, official guide paths, source URLs, phase/lesson/chapter hints, or answer-source breadcrumbs.
- Source URLs, screenshots, and gold extraction notes belong in private reference/audit materials only.
- Tasks must be GUI-dependent, expert-hours, and submission-judgeable from structured artifacts where possible.

## Porting checklist
- Update `openclaw_profile/USER.md` for the new operator.
- Review `openclaw_profile/SOUL.md` and `AGENTS.md` for local behavior.
- Keep the anti-leak prompt policy intact.
- Set `AGENTHLE_BENCHMARK_ROOT` and optionally `OPENCLAW_SCALEUP_OUT` when using export scripts on a different machine.
- Treat paths embedded in `reports/` as historical audit traces from the source machine, not as required runtime paths for the new machine.
