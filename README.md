# GrantDedup

A bounded semantic overlap registry for curated grant cohorts. It checks each enrolled proposal against every earlier proposal and preserves a structured audit trail of duplicate work versus substantive extensions.

## Why GenLayer

Hash-based registries cannot detect paraphrased scope. A centrally hosted embedding filter can omit relevant comparisons and usually conflates shared infrastructure with duplicated deliverables. Here the contract fixes the candidate set and validators independently agree on every pairwise relation.

## State and authority

The deployer is the immutable curator. `entries` is an append-only array of at most 16 proposal records, each ≤3,000 characters, attributed by the curator to an applicant address. `reviews[entry_id]` stores prior hashes, complete-prefix length, per-pair relations/citations and deterministic outcome. No entry can be edited or deleted.

## Lifecycle

`enroll → review once`. Entry n must compare with all entries 0..n−1, including entries that have not yet been reviewed. It never waits for their AI outcome. Enrollment order is fixed before each review. Entry zero is eligible relative to the empty prefix without an LLM call.

## Consensus and equivalence

The contract constructs the full earlier prefix from state. The leader and validators independently assign DUPLICATE, EXTENSION, DISTINCT or UNKNOWN to every pair. Ordered relation vectors must match exactly; quote wording may differ. Each non-UNKNOWN pair requires actual excerpts from both proposals. Deterministic aggregation gives DUPLICATE if any pair duplicates prior scope; otherwise REVIEW if any pair is UNKNOWN; otherwise ELIGIBLE. EXTENSION means a substantial new deliverable, not a renamed token or project.

Malformed outputs, invented citations, incomplete arrays or disagreement are rejected. Each accepted receipt records the leader's validated evidence; independently produced validator explanations are not stored. The decision equivalence is substantive, not a JSON-format check.

## Public API

Constructor: no arguments. Source: [contract.py](contract.py). RPC-checked ABI: [schema.json](schema.json).

| Method | Caller | Meaning |
| --- | --- | --- |
| `enroll(applicant: Address, proposal)` | Curator | Append immutable proposal; assigned ID is previous count |
| `review(entry_id)` | Anyone | Compare to all earlier entries and commit one review |
| `get_entry(entry_id)` | Read | Proposal, applicant attribution and content hash |
| `get_review(entry_id)` | Read | Complete pairwise review |
| `count()` | Read | Enrolled entries |

## Example walkthrough

1. Curator enrolls applicant A with: “Build an open-source offline-capable merchant wallet with QR payments and a transaction CSV export. Deliver the mobile source and a deployment guide.”
2. Curator enrolls applicant B with the same scope paraphrased under a different product name. IDs are 0 and 1.
3. Call `review(1)`. A good live consensus run should classify the pair as DUPLICATE. Read `get_review(1)` and inspect the citations.
4. Enroll applicant C with a clearly additional deliverable, e.g. a separately specified accessible hardware terminal integration, while explicitly declaring the reused wallet. Review ID 2: all prior proposals must be included, with EXTENSION where justified.
5. Also test an underspecified “build a better wallet” proposal: it must not become DISTINCT simply because it omits detail.

Each write is a separate transaction. For this walkthrough, wait for the successful state needed by the next call. The batch deploy script skips AI confirmation only because these four constructors are independent.

## Tests and review

Run `python -m unittest discover -s tests -p 'test_*.py' -v` from this repository root. Tests load this exact source through a small fake GenVM adapter and exercise role checks, history/immutability, malicious model outputs and independent disagreement. They are logic tests, not live model consensus tests. See [VALIDATION.md](VALIDATION.md).

## Limitations

This is cohort-local scope overlap, not global uniqueness, Sybil resistance, plagiarism detection or proof of ownership. Curator attribution is not an applicant signature. The curator can manipulate ordering or admission; no earliest-on-the-internet claim is made. ELIGIBLE only means no duplicate in the checked prefix, not deserving funding. Full-prefix comparisons bound worst-case input to about 48,000 characters but still need cost profiling. To exceed 16 entries, design audited batching/indexing rather than silently truncating comparisons.

## Deployment and integration

Deploy this file independently, with zero constructor arguments and full consensus (`leaderOnly: false`). The repository contains the contract, English documentation and tests only. Deployment tooling is maintained separately. After publication, `deployment.json` records this contract's observed Bradbury transaction. Transaction existence does not prove successful execution or finality. Consumers should read finalized successful receipts and bind them to this contract address and their own business rules.

Category: **Intelligent Contracts**. Suggested submission text: [SUBMISSION.md](SUBMISSION.md). MIT license.
