# Lightweight Review Checklist

Use only the sections relevant to the change. A small documentation correction does not need a full software release audit.

## Purpose and scope
- [ ] The change addresses a clear problem or user outcome.
- [ ] Scope is proportionate and avoids unrelated refactoring.
- [ ] Confirmed decisions, assumptions, and open questions are distinguishable.

## Safety and security
- [ ] Inputs, permissions, trust boundaries, scripts, dependencies, and network behavior were considered where relevant.
- [ ] No secrets or privileged credentials are exposed.
- [ ] CI and automation use least privilege and trusted, pinned dependencies.
- [ ] Failure, rollback, and recovery behavior are understood where relevant.

## Legal, privacy, and publication
- [ ] Rights and licence compatibility are understood for contributed material.
- [ ] Personal data, confidential content, and identifying metadata have been reviewed.
- [ ] Privacy and legal claims match actual behavior and evidence.
- [ ] Required notices, attribution, and disclosures are present.

## Usability and trust
- [ ] Instructions are understandable and accessible to the intended audience.
- [ ] User-visible behavior and trade-offs are explained.
- [ ] Claims are evidence-backed; limitations are explicit.
- [ ] User choice and portability are preserved where feasible.

## Validation and release
- [ ] Relevant tests and checks were run and results recorded.
- [ ] Unrun checks and known limitations are stated.
- [ ] Documentation and handover are current.
- [ ] Residual risks and required approvals are recorded.
- [ ] The authorized owner has made any required release or merge decision.
