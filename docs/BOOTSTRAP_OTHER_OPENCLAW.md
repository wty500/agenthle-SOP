# Bootstrap on another OpenClaw instance

1. Create or choose the target workspace.
2. Copy files from `openclaw_profile/` into the workspace root.
3. Copy `docs/` into the workspace docs area (or keep this repo adjacent and reference directly).
4. Read in this order:
   - `openclaw_profile/SOUL.md`
   - `openclaw_profile/USER.md`
   - `docs/agenthle_task_acquisition_sop_draft.md`
   - `docs/gpt5pro_prompt_sop_for_domain_packs.md`
5. Before packaging tasks for public use, run a prompt-source-leak scan and manually review any hits.
6. Use `scripts/` as templates for packaging domain bundles and manifests.
7. If you use the export helpers, point `AGENTHLE_BENCHMARK_ROOT` at your local benchmark root; optionally set `OPENCLAW_SCALEUP_OUT` for the output directory.
8. Ignore absolute paths shown in historical `reports/` files unless you are explicitly auditing the source machine's past outputs.
