# MANIFEST — Carpathia Assignment Solver v7.0.0 run

**Run status:** `HALT — COMPLETE` (all phases rendered, all gates pass).

**Run:** `assignment-solver-2026-10-04` · runtime mode `TOOLS_PRESENT` · adapter status `MAPPED` · fallback mode `false`

## Inputs (verified, read-only)

| Input | Path | sha256 |
|---|---|---|
| Assignment brief | `ASSIGNMENTS/GEN_AI/project_3.yaml` | `5f641d01f096e6a1de5b2654da30bc6048085999214ce203fcb93388bae39cc0` |
| Assignment-1 research pack | `ASSIGNMENTS/GEN_AI/project_3_research.yaml` | `88a687279df66203dc86f5ba3b96860e5207149d6a7bd25a04c1f0f8d4c3f5b1` |
| Chart analysis package (source) | `QMDJ/GEN_AI/project_3.json` | `20dc73a91a46c4dca78cca6fc9bc7520b91c7b16d9edb18fb93f76d1e8360a15` |
| Chart analysis package (sealed deliverable) | `SUBMISSION/GEN_AI/project_3/package/seal.json` | 58 artefacts, self-verified |

The raw chart source was never opened by this run; the package was consumed read-only under guard.

## Result

- Direction selected: **Guarded Pact — the shipped direction** (`BSC-001`), requirement fit 0.9328, final score 0.9048
- Requirements: 34 facets — 24 required, 4 prohibitions, 6 should-level
- Coverage gate: **PASS** (declared input substitutions: 2) | lint: **CLEAN** | gates all pass: **True**
- Artefacts in this manifest: **67**, plus this manifest itself

## Artefacts (sha256)

| Path | sha256 |
|---|---|
| `ANNOTATED/01_brief_1_brand_idea_and_philosophy.annotated.md` | `eca69d7acc5fd4aeae187d631629899a1eee324b3d986181484409897b6c3544` |
| `ANNOTATED/02_brief_2_product_and_packaging.annotated.md` | `a5b3ec668739cc0d7288910676fc6395a2a8a32eeb425293894be95e39d3ad80` |
| `ANNOTATED/03_brief_3_ad_campaign.annotated.md` | `e4f75e8fef7d5f23332cfec19e7d57909c74ca724a8988d2ce6dca1e6f37dac0` |
| `ANNOTATED/position_in_wider_answer.md` | `a3c5170e3505a0ab8d5a6bd7b730a8cbae9ffd94fefef3828a0086462c24d82c` |
| `ANNOTATED/response_map.md` | `94faee7f978dbeda20ba3ca37eb21bdc92534d3c354155203762d313e364f4c0` |
| `LAYER_A/01_executive_reading.md` | `2b141e69f13dcda9b6655302d0be6e2f244434165da8697368047d12f32f6ca3` |
| `LAYER_A/02_walkthrough.md` | `83d7aa93464a449bd041969d6368447881b606625ca92517fecee3c8dfe31143` |
| `LAYER_A/03_candidates_and_selection.md` | `a3390bca65bd93fbe6eb83262b45855fb97ed71ccc675550629addebc91d2dd1` |
| `LAYER_A/04_confidence_and_residual_risk.md` | `cbc5748a942a5df8cf61ecf1561a65ab97e085c1b452b16a845e7ee921d4005b` |
| `LAYER_A/05_full_technical_mapping.md` | `6c7b2639bf4869b54088dc3d33d13ab05ab5135b1c81c0182a2b5b2682c381ca` |
| `OPERATOR/ADAPTER/adapter_map.json` | `79bf0f63944dc0e3cfa5c2ec1efdced7bdb05cbc6b2b362b20a174bc196e7368` |
| `OPERATOR/ADAPTER/adapter_report.md` | `7b0128917180a565b6e8db49d4d57d4b05cb5de175ead63f4186cd9f26fc1975` |
| `OPERATOR/ANOMALY_LOG.md` | `914ed95976b4c02b5123528cf6bec4b9afa633923c60824603efa5c07dea0a1e` |
| `OPERATOR/CALL_LOG.jsonl` | `d3720269e2a451efed043051d5210cec15c06401531bc2c82bdfa3978e4d6ed7` |
| `OPERATOR/GAP_REGISTER.md` | `dade6b30a28fbc7c1a22f62d6759a4b86b4edb4f1082283db2d06c7ab2c87ee5` |
| `OPERATOR/HARD_CONSTRAINT_VETO.md` | `603bd66e13223879a60d0abe409061ee25db5669f5bed31b2c80730010aba7ed` |
| `OPERATOR/SOURCE_HASHES.json` | `830bdbb461158fe8842ceb094a4e8cf2bb1cb00fb4ffd8f765c6e1f06dce3505` |
| `OPERATOR/STATE/logs/ADAPTER/read_log.json` | `f4e494719d5bf6ee7630f0151816797a88d489d4112c5ceddd0c7851e5597dbc` |
| `OPERATOR/STATE/logs/ADAPTER/write_log.json` | `f36d426d2dd3b8095123ea5307db57512c8ce2ea7f3a3727fc0224911d2a1dcf` |
| `OPERATOR/STATE/logs/FINALIZE/read_log.json` | `8b5c4922a04a4c63b21cdd2265744a9242379b84433534d6b9cf1a253b020463` |
| `OPERATOR/STATE/logs/FINALIZE/write_log.json` | `bd5de91af940dc59ac77fcd047a845d87fb44810d40d10c9f3267a81fce2779c` |
| `OPERATOR/STATE/logs/INGEST/read_log.json` | `861f4592ea0aac70c0e98a6eb9fd8555dd1fe2228a5ae1123c62828c7dc64003` |
| `OPERATOR/STATE/logs/INGEST/write_log.json` | `24a708c4be3a09888371a63e6b9a06e27fa0cb4f1b3834fda7e3762b39b89237` |
| `OPERATOR/STATE/logs/RENDER/read_log.json` | `aadf1a567b6a82812d73955ba9aca141ec6cbe6fd2ab2e999aa4c2414d831de5` |
| `OPERATOR/STATE/logs/RENDER/write_log.json` | `78c88c0686785aa457dc336ace8fe9b2278603111e265e081d86963b024c12d3` |
| `OPERATOR/STATE/logs/SOLUTION/read_log.json` | `8c8a005b5e457b844ec0aae742c17edc3c7ce473685ea824d45c6df4cc36e776` |
| `OPERATOR/STATE/logs/SOLUTION/write_log.json` | `7ca63f77340d223b1695f362f6713b64baac18f505f1df80165146dec8224f0b` |
| `OPERATOR/STATE/machine_state.json` | `16de655be367e806d0a7b061a76107a399015a39b616135c80630102a852efba` |
| `OPERATOR/STATE/pdf_ingest.json` | `62ee96cea59ea3627a8237f5d23cd2825c6457697d326a36ca2279a68b2b2d1e` |
| `OPERATOR/STATE/second_tally.md` | `c383f41f414cf912bf38c46c629432960305021df26ed391ba222a70e35f7d48` |
| `OPERATOR/VERIFICATION/gates.json` | `243cae26a1a311124ebfb743fe658d55c428f2a804feb67c2be65592024af086` |
| `OPERATOR/VERIFICATION/layer_a_contract.json` | `5f31b933e1db08ee881e1892c14e471ef2bb1b9caf61a43195c7d2e6f21e5c70` |
| `OPERATOR/VERIFICATION/lint_report.md` | `49eb251c474e1a32e48ab6f5f372966fdeaca2148d966f92d2ffec182779509d` |
| `OPERATOR/VERIFICATION/proof.md` | `a4564ce5e47f91f1375532c74a10831eba479b97671130c13e8a77555207c478` |
| `OPERATOR/VERIFICATION/red_team.json` | `751ea463dd8b4fa43a319551d917f43c22c9a45c0c6f1929cd96c454c3773831` |
| `OPERATOR/VERIFICATION/red_team.md` | `e6dd9f596478d5c8f5770c70ce76242686756e8cf25f7839987f006dd7dbe4da` |
| `README.md` | `217ee77b70ffb09b113dca6c9192f4273aa9e7c8a3d3d672f90f46560b2ce091` |
| `SUBMISSION/00_cover_and_index.md` | `d4d072bfa13279139022508be91573cfa52f77c6cd8d8549fa2a7032540ff818` |
| `SUBMISSION/01_brief_1_brand_idea_and_philosophy.md` | `99fa1599ae69925c947ac9b9a5784dd417ff6d94c20c921e51ca7d3f374f59e0` |
| `SUBMISSION/02_brief_2_product_and_packaging.md` | `0a69619943db2bf09004c702c57e3ea90674ad0163f7230ffbb45a72b7ca61c4` |
| `SUBMISSION/03_brief_3_ad_campaign.md` | `bc6a4dd66f1b482f75890d6227a0995cc93b46680810f3418f5b8cedeea888a6` |
| `SUBMISSION/04_coherence_check.md` | `d753bee1a71ad0f99b881aff51180331cc20da44284a9d47d18091a4c81fd527` |
| `SUBMISSION/05_logline.md` | `75f3f21bbf0bc8943fa32b190f7ab8867fca1aa7a162f0f569fbdbd934b45536` |
| `SUBMISSION/06_mood_board_index.md` | `8e4af8fb73821c160469d253ca1149808f1ba296d4ac680f0fa52d2317f4c318` |
| `SUBMISSION/07_production_and_ai_workflow.md` | `aad6209e3a6bee4ae85c98275ea3d67e8e2af00fe1fad4ef83fbe55883fa9aaa` |
| `SUBMISSION/08_risks_and_how_they_are_handled.md` | `d1c82b7c33bb053471e114eff3de674fe28af094ab4aba9773b567c6e3ad6fcb` |
| `SUBMISSION/09_research_reference_index.md` | `92e9ff12cc52842feddd9a4d9a71ac773a66decaab4860063f94aa61f447f79b` |
| `config/scoring.yaml` | `3584e4d894aeaa6eabeeda71b7fa929c3e14083e9039ff251536e96d71e14051` |
| `raw/assignment_1_research.yaml` | `88a687279df66203dc86f5ba3b96860e5207149d6a7bd25a04c1f0f8d4c3f5b1` |
| `raw/assignment_brief.yaml` | `5f641d01f096e6a1de5b2654da30bc6048085999214ce203fcb93388bae39cc0` |
| `tools/adapter.py` | `037eedb12bd39162ad2dea754be8dd507a2a72a7f90cca468f3e5ef766b7f698` |
| `tools/finalize.py` | `e365713c2dd451da7ca9e1b54f5d5d5a6ff63e242a0265988d817552b58f45f2` |
| `tools/guarded.py` | `c25a12ca4f3d7842a8896a6585e81a95008f97309f7d33968a9789833c7f14c7` |
| `tools/render.py` | `7df915d3e85614a88c3239688c6c17cff8126bd1ac50a5f3603cf2863c8fb314` |
| `tools/requirements.py` | `80e6d8ef01e3afeb78073c21b480364ba0e9f0c92980477f77e3ae6a213a44c2` |
| `tools/solve.py` | `3baf12316e351acce724261304ea76e8329af43e794786604dddf01cfea52e86` |
| `work/adapted_package_view.json` | `ea5296f17a2fedef3cc54f6df1dff4638dc8c725a2ce36df6b7270cc1227c5ea` |
| `work/bindings.json` | `be47f1b7b19df75e6b1edd6498be7f7be31595ddcb1f17b80e858817c941b925` |
| `work/bindings_ledger.json` | `22c32b4b9c8dcba53a2855dfccca56af8e3477c49625fb300e2759fc84280c7f` |
| `work/candidates_scored.json` | `b2f88e7778c1128f244e58df1da38c59e5e97ccdd311b92db9e70090274a23fb` |
| `work/cmap.jsonl` | `6567b44808f2fcf4996a8132a0250c6e992bf65ccd21f5809299f05b1590f65b` |
| `work/evidence_ledger.json` | `2c28b7d0a1640649824057f519454ff5688500e6b7bd8f686a07cc35310483b3` |
| `work/gates.json` | `2d74de54330acb091fca78af1dd753a3c883627da84f3002e28035329314f778` |
| `work/hidden_problems_resolved.json` | `ae3d68a8edb8100c1f57880487a9fabf73df5c6b9659557fafab68742ce74666` |
| `work/requirement_ledger.json` | `2fc2045c9ef0b9b7825fe04f079e7e9eb15be443ff90dad242ec68b91866215c` |
| `work/requirements.json` | `2b0592555469dd410fa8e0c782461b4698838eef15c7941cef7c6eaea8deb243` |
| `work/research_index.json` | `61082a61494e3c3479922e65ccce41e48f437ce995b89abf97c3ead6c4e19354` |

## How to reproduce

```bash
cd SUBMISSION/GEN_AI/project_3_solution/tools
python3 requirements.py     # decompose the brief, index the research
python3 adapter.py          # adapt the sealed analysis package
python3 solve.py            # bindings, ledger, scoring, gates
python3 render.py           # submission + annotated
python3 finalize.py         # operator pack, layer A, lint, manifest
```

The manifest is written last and hashes every artefact above it; re-running the chain reproduces the same artefact set with the same digests (JSON key order and text rendering are deterministic).
