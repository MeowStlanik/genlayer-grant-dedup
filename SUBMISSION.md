# GrantDedup — standalone Intelligent Contract

**Category:** Intelligent Contracts

**Purpose:** A bounded semantic overlap registry for curated grant cohorts. It checks each enrolled proposal against every earlier proposal and preserves a structured audit trail of duplicate work versus substantive extensions.

**Why consensus matters:** The contract constructs the full earlier prefix from state. The leader and validators independently assign DUPLICATE, EXTENSION, DISTINCT or UNKNOWN to every pair. Ordered relation vectors must match exactly; quote wording may differ. Each non-UNKNOWN pair requires actual excerpts from both proposals. Deterministic aggregation gives DUPLICATE if any pair duplicates prior scope; otherwise REVIEW if any pair is UNKNOWN; otherwise ELIGIBLE. EXTENSION means a substantial new deliverable, not a renamed token or project.

**State design:** The deployer is the immutable curator. `entries` is an append-only array of at most 16 proposal records, each ≤3,000 characters, attributed by the curator to an applicant address. `reviews[entry_id]` stores prior hashes, complete-prefix length, per-pair relations/citations and deterministic outcome. No entry can be edited or deleted.

**Reusable beyond a demo:** Hash-based registries cannot detect paraphrased scope. A centrally hosted embedding filter can omit relevant comparisons and usually conflates shared infrastructure with duplicated deliverables. Here the contract fixes the candidate set and validators independently agree on every pairwise relation.

**Source:** `contract.py` (self-contained; zero-argument constructor).

**Review materials:** project README, ABI schema, `tests/test_contract.py` and `VALIDATION.md`.

**Deployment evidence:** after publication, use this repository’s `deployment.json`. It proves an observed matching transaction, not final success. Add the actual repository URL, successful deployment address and live invocation transaction IDs when submitting. Those values are intentionally not fabricated in this draft.

**Current verification scope:** local logic tests and Bradbury schema loading. Live AI consensus and production audit remain outstanding. This is cohort-local scope overlap, not global uniqueness, Sybil resistance, plagiarism detection or proof of ownership. Curator attribution is not an applicant signature. The curator can manipulate ordering or admission; no earliest-on-the-internet claim is made. ELIGIBLE only means no duplicate in the checked prefix, not deserving funding. Full-prefix comparisons bound worst-case input to about 48,000 characters but still need cost profiling. To exceed 16 entries, design audited batching/indexing rather than silently truncating comparisons.
