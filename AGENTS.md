# AGENTS.md — Staged, User-Authorized Workflow

## Core Rule: No Unapproved Repository Access

**Do not open, read, search, enumerate, index, or otherwise inspect any repository file unless the user has explicitly identified that file's role, purpose, and intended use for the current stage.** A path appearing in another file, a README, a directory listing, a previous task, or an agent's assumption does not authorize access.

At the start of a task, use only:
- this instruction file as the workflow policy; and
- the exact repository paths the user has explicitly designated for the current stage and explained how to use.

Do not read `README.md`, `AGENT.md`, other prompts, sibling assignment files, other charts, scripts, configuration, generated files, or directory contents just to gain context. Do not run broad search, tree, glob, or discovery commands. Do not infer authorization from a filename alone. If a required input is missing or inaccessible, stop that branch of work and report the specific missing path; do not look for a substitute unless the user authorizes it.

Authorization is **stage-specific**. A file authorized for one stage is not automatically authorized for a later stage, and authorization to read a file does not authorize editing it. Only create, edit, or delete files that the user has asked you to create, edit, or delete, plus necessary outputs inside the explicitly designated task workspace.

The filenames in examples below are not fixed. For every assignment, use the exact paths and roles the user states in that task. The user's explicit mapping overrides example names and default conventions.

## The Two-Stage Task Contract

This repository's assignment workflow is normally split across two separate user prompts. Do not collapse the stages or pre-read files needed only by the next stage.

### Stage 1 — QMDJ Chart Analysis

The user identifies:
- a QMDJ chart file and says to use it as the chart;
- a case-context file and says to use it as `case_context`;
- a QMDJ chart analyst charter and says to use it as the role/system prompt for this stage; and
- a destination under `SUBMISSION/{track}/{slug}/` in which to create a folder and work.

For this stage:

1. Read **only** the user-designated chart, case-context file, and chart-analyst charter. Do not open the assignment-solver charter or any other file unless the user has separately authorized it for this stage.
2. Apply the chart-analyst charter as the governing task role for the analysis, within higher-priority platform and safety instructions. Do not replace it with a different charter or blend in an unauthorized prompt.
3. Create and work in the user-designated submission workspace. Keep stage outputs, working notes, structured analysis, and evidence references inside that workspace. Do not use a different project folder or write elsewhere in the repository.
4. Complete the chart analysis before treating Stage 1 as complete. Preserve traceability to the designated chart: distinguish explicit chart data from computed results and inference; retain relevant JSON paths; record constraints, uncertainty, contradictions, and the architecture-compatible possibilities the chart supports. Do not invent chart fields or convert inference into explicit chart fact.
5. Save a durable, clearly named QMDJ analysis artefact in the designated workspace. Include enough reasoning, evidence references, and usable conclusions for Stage 2 to rely on it without reopening the original chart. Keep intermediate files in that workspace as well.
6. Do not start completing the assignment as though the assignment-solver charter were active. Do not inspect files merely because the chart or case context mentions them. Report the analysis artefacts created and any genuine input limitation.

The chart, case context, charter, track, slug, and output names are task inputs, not constants. For example, paths such as `QMDJ/ADVERTISING/project_2.json`, `ASSIGNMENTS/ADVERTISING/project_2.yaml`, `PROMPT/qmdj_chart_analyst_charter.md`, and `SUBMISSION/ADVERTISING/project_2/` are illustrative only; follow the exact paths designated by the user.

### Stage 2 — Assignment Execution

Stage 2 begins only when the user gives the next task and identifies the assignment-solver charter, assignment brief, and completed QMDJ analysis to use.

For this stage:

1. Switch the active task role to the **user-designated assignment-solver charter**. Do not keep using the chart-analyst charter as the active role; the completed analysis produced in Stage 1 is now the reference artefact.
2. Read only the files authorized by the Stage 2 prompt: normally the assignment-solver charter, the named assignment/case-context file, and the Stage 1 QMDJ analysis inside the designated submission workspace. Do not reopen the original QMDJ chart or inspect other repository files by default. The user said to rely solely on the complete QMDJ analysis; respect that boundary.
3. Treat the assignment brief as the source of deliverable requirements, audience, constraints, and assessment criteria. Use the completed QMDJ analysis as the sole QMDJ evidence source. Do not invent analysis that is absent from it or imply that the original chart was rechecked.
4. Produce the complete assignment deliverables in the user-designated `SUBMISSION/{track}/{slug}/` workspace. Match the artefacts and format the brief actually calls for; do not impose a generic template if it conflicts with the brief. Keep drafts, notes, and final artefacts within the authorized workspace.
5. Keep client-/marker-facing assignment content distinct from internal technical analysis when the brief calls for that separation. Do not expose QMDJ jargon, operator mappings, or internal evidence notes in the submitted artefact unless the brief expressly requires them.
6. **Ask the user decision-focused questions with viable options that fit the architecture established by the completed QMDJ analysis.** Ask only about material preferences or missing facts that cannot be reliably derived from the authorized brief and analysis. Each option must be genuinely feasible under the identified constraints; state meaningful trade-offs where useful. Do not offer options contradicted by the analysis, present a chart-incompatible option as viable, or use leading questions to force a predetermined answer.
7. Do not ask the user to restate information already contained in the authorized files. Complete the portions that are already determined. If a decision materially affects the final deliverable, surface the question and chart-compatible options at the point where the answer is needed; proceed with independent work and clearly label any provisional choice rather than fabricating the user's preference.
8. Before reporting completion, check the deliverables against the brief, verify internal consistency with the Stage 1 analysis, and disclose any unresolved choices or limits. Never claim perfection or validation that was not actually established.

Stage 2 does not grant permission to read all of `SUBMISSION/`, all of `ASSIGNMENTS/`, or all of `QMDJ/`. Access only the particular files necessary and expressly authorized for this stage.

## Role-Prompt Handling

The user may designate prompt files as the role/system prompt for a stage. Read and apply only the prompt the user authorized for that stage, as task-level instructions subordinate to platform and safety requirements. Switching stages means switching to the newly designated role prompt; it does not authorize reading additional prompts.

Do not read or apply a charter early merely because this file names it as a possible Stage 2 input. Do not edit charters, briefs, charts, or case-context files unless the user explicitly requests that edit.

## Workspace, Paths, and File Hygiene

- Use the exact workspace provided by the user, normally `SUBMISSION/{track}/{slug}/`.
- Create subfolders within that workspace only when they serve a clear purpose, and keep all task-created artefacts there unless the user directs otherwise.
- Preserve user-provided track/slug spelling and filenames. Example paths are illustrative; task-specific paths may vary.
- Do not flatten or rename the user's input structure.
- Keep source inputs unchanged. Never silently edit the chart, brief, case-context file, or role prompt while executing the assignment.
- Do not copy generated scratch into other repository locations, and do not inspect `.gitignore` or other project configuration unless the user authorizes it.
- Make focused changes. Do not reformat or alter unrelated files.

## Evidence, Questions, and Reporting

Maintain clear boundaries between:
- **Explicit:** directly stated in a user-authorized source.
- **Computed:** derived from explicit source data by a stated method.
- **Inferred:** a reasoned interpretation, with uncertainty preserved.
- **User decision:** a preference or fact that must come from the user.
- **Unverified:** something that could not be confirmed from authorized materials.

For chart-based recommendations, give only options that are supported by or compatible with the Stage 1 analysis, and make uncertainty visible. If the authorized inputs conflict or leave a critical gap, explain the precise issue; do not resolve it by opening unauthorized files or fabricating facts.

At each stage's end, report the workspace path, artefacts created or updated, checks actually performed, questions or provisional decisions requiring user input, and any blockers. Keep that report specific to the current stage.
