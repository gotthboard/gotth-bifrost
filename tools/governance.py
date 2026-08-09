#!/usr/bin/env python3
"""Validate and render Bifrost meta-repository governance data.

This dependency-free tool validates metadata, documentation consistency, and
representative JSON contract fixtures. It does not validate runtime behavior,
cryptographic signatures, or external evidence contents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import tomllib
from collections.abc import Iterable
from datetime import datetime
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
REQ_RE = re.compile(r"^\- \*\*(BFW-PRD-\d{3}):\*\*", re.MULTILINE)
MAP_RE = re.compile(r"^\| (BFW-PRD-\d{3}) \|", re.MULTILINE)
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class Findings:
    """Collect all validation errors so one run gives a complete repair list."""

    # Complexity: time O(1), Omega(1), tight Theta(1); auxiliary space O(1),
    # Omega(1), tight Theta(1), excluding later retained findings.
    def __init__(self) -> None:
        self.errors: list[str] = []

    # Complexity: time O(len(message)), Omega(len(message)), tight Theta(len(message));
    # auxiliary space Theta(len(message)); the copied message is retained once.
    def add(self, message: str) -> None:
        self.errors.append(message)

    # Complexity: time and auxiliary space O(1), Omega(1), tight Theta(1).
    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.add(message)


# Complexity: time O(n), Omega(n), tight Theta(n) in file bytes n; auxiliary
# space O(n), Omega(n), tight Theta(n) for parsed TOML; filesystem I/O is linear.
def load_toml(relative: str) -> dict[str, Any]:
    with (ROOT / relative).open("rb") as handle:
        return tomllib.load(handle)


# Complexity: time O(n), Omega(n), tight Theta(n) in file bytes n; auxiliary
# space O(n), Omega(n), tight Theta(n) for parsed JSON; filesystem I/O is linear.
def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# Complexity: time O(n), Omega(n), tight Theta(n) in file bytes n; auxiliary
# space O(1), Omega(1), tight Theta(1) with fixed-size streaming buffers.
def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


# Complexity: time O(n), Omega(n), tight Theta(n) in text length n; auxiliary
# space O(k), Omega(k), tight Theta(k) for k matched identifiers.
def extract_ids(pattern: re.Pattern[str], text: str) -> list[str]:
    return pattern.findall(text)


# Complexity: time O(d), Omega(1), tight Theta(d) for d cited digests;
# auxiliary space O(1), excluding caller-owned mappings.
def has_requirement_bound_evidence(
    requirement_id: str,
    digests: list[str],
    evidence_scopes: dict[str, set[str]],
) -> bool:
    return any(requirement_id in evidence_scopes.get(digest, set()) for digest in digests)


# Complexity: time O(r log r + p + m), Omega(r + p + m), where r is trace
# records and p/m are PRD/map bytes; auxiliary space O(r).
def validate_requirements(findings: Findings) -> dict[str, Any]:
    registry = load_toml("governance/requirements.toml")
    traces = registry.get("requirements", {})
    prd_text = (ROOT / "documents/PRD.md").read_text(encoding="utf-8")
    spec_text = (ROOT / "documents/IMPLEMENTATION-SPEC.md").read_text(encoding="utf-8")
    prd_ids = extract_ids(REQ_RE, prd_text)
    map_ids = extract_ids(MAP_RE, spec_text)
    trace_ids = list(traces)

    findings.require(len(prd_ids) == len(set(prd_ids)), "duplicate requirement definition in PRD")
    findings.require(len(map_ids) == len(set(map_ids)), "duplicate requirement verification-map row")
    findings.require(set(prd_ids) == set(map_ids) == set(trace_ids), "PRD, verification map, and trace registry ID sets differ")
    if trace_ids:
        expected = [f"BFW-PRD-{index:03d}" for index in range(len(trace_ids))]
        findings.require(sorted(trace_ids) == expected, "requirement IDs are not contiguous from BFW-PRD-000")

    required = {"owner", "status", "blocking_dependencies", "verification_commands", "evidence", "admission"}
    allowed_status = {"defined", "active", "blocked", "verified", "retired"}
    allowed_admission = {"not_admitted", "admitted", "rejected", "revoked"}
    catalog = load_toml("governance/components.toml")
    known_owners = {"meta"} | {entry["id"] for entry in catalog.get("components", [])} | {entry["id"] for entry in catalog.get("external_dependencies", [])}
    known_blockers = set(trace_ids) | known_owners | {"BFW-ALPHA-0", "BFW-PHASE-0"}
    governance_evidence: dict[str, set[str]] = {}
    for path in (ROOT / "workflow/features").glob("*/evidence/verification.toml"):
        if not path.is_file():
            continue
        evidence = tomllib.loads(path.read_text(encoding="utf-8"))
        digest = sha256_file(path)
        declared = evidence.get("requirements", [])
        findings.require(isinstance(declared, list) and bool(declared), f"{path.relative_to(ROOT)}: evidence requirement scope is empty")
        findings.require(set(declared) <= set(trace_ids), f"{path.relative_to(ROOT)}: evidence references unknown requirement")
        findings.require(len(declared) == len(set(declared)), f"{path.relative_to(ROOT)}: duplicate evidence requirement")
        governance_evidence[digest] = set(declared)
    for requirement_id, record in traces.items():
        findings.require(required <= set(record), f"{requirement_id}: missing trace fields {sorted(required - set(record))}")
        findings.require(record.get("status") in allowed_status, f"{requirement_id}: invalid status")
        findings.require(record.get("admission") in allowed_admission, f"{requirement_id}: invalid admission")
        findings.require(record.get("owner") in known_owners, f"{requirement_id}: unknown owner")
        for field in ("blocking_dependencies", "verification_commands", "evidence"):
            findings.require(isinstance(record.get(field), list), f"{requirement_id}: {field} must be an array")
        findings.require(set(record.get("blocking_dependencies", [])) <= known_blockers, f"{requirement_id}: unknown blocker")
        for digest in record.get("evidence", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{requirement_id}: invalid evidence digest")
        if requirement_id >= "BFW-PRD-079" and record.get("status") == "verified":
            bound = has_requirement_bound_evidence(requirement_id, record.get("evidence", []), governance_evidence)
            findings.require(bound, f"{requirement_id}: verified governance trace lacks requirement-bound current evidence")
        if record.get("admission") == "admitted":
            findings.require(record.get("status") == "verified", f"{requirement_id}: admitted trace must be verified")
            findings.require(bool(record.get("verification_commands")), f"{requirement_id}: admitted trace lacks executable verification")
            findings.require(bool(record.get("evidence")), f"{requirement_id}: admitted trace lacks evidence")
    return registry


# Complexity: time O(v + e), Omega(v), tight Theta(v + e) for v graph vertices
# and e dependency edges; auxiliary space O(v) for colors and recursion stack.
def find_dependency_cycle(graph: dict[str, list[str]]) -> list[str]:
    state: dict[str, int] = {}
    stack: list[str] = []

    # Complexity: across one DFS, time O(v + e), Omega(1) per call and tight
    # aggregate Theta(v + e); auxiliary recursion/stack space O(v).
    def visit(node: str) -> list[str]:
        state[node] = 1
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if state.get(dependency) == 1:
                return stack[stack.index(dependency) :] + [dependency]
            if state.get(dependency, 0) == 0:
                cycle = visit(dependency)
                if cycle:
                    return cycle
        stack.pop()
        state[node] = 2
        return []

    for component in graph:
        if state.get(component, 0) == 0:
            cycle = visit(component)
            if cycle:
                return cycle
    return []


# Complexity: time O(c + e), Omega(c), tight Theta(c + e) for c components and
# e dependency/conflict edges; auxiliary space O(c + e) for indexes and graph.
def validate_components(findings: Findings) -> dict[str, Any]:
    catalog = load_toml("governance/components.toml")
    components = catalog.get("components", [])
    externals = catalog.get("external_dependencies", [])
    platform_policy = catalog.get("platforms", {})
    known_platforms = set(platform_policy.get("known", []))
    admitted_platforms = set(platform_policy.get("admitted", []))
    component_ids = [entry.get("id") for entry in components]
    external_ids = [entry.get("id") for entry in externals]
    findings.require(len(component_ids) == len(set(component_ids)), "duplicate component ID")
    findings.require(len(external_ids) == len(set(external_ids)), "duplicate external dependency ID")
    known = set(component_ids) | set(external_ids)
    records_by_id = {
        entry.get("id"): entry
        for entry in components + externals
        if entry.get("id")
    }
    findings.require(admitted_platforms <= known_platforms, "catalog admits unknown platform")
    required = {
        "id", "kind", "responsibility", "repository", "revision",
        "artifact_digests", "api_version", "schema_version", "ui_version",
        "dependencies", "conflicts", "platforms", "platform_status",
        "migration_order", "rollback_mate", "evidence_hashes", "status", "admission",
    }
    graph: dict[str, list[str]] = {}
    for entry in components:
        component_id = entry.get("id", "<missing>")
        findings.require(required <= set(entry), f"{component_id}: incomplete component record")
        dependencies = entry.get("dependencies", [])
        conflicts = entry.get("conflicts", [])
        platforms = entry.get("platforms", [])
        findings.require(all(item in known for item in dependencies), f"{component_id}: unknown dependency")
        findings.require(all(item in known for item in conflicts), f"{component_id}: unknown conflict")
        findings.require(component_id not in dependencies, f"{component_id}: self dependency")
        findings.require(component_id not in conflicts, f"{component_id}: self conflict")
        findings.require(len(platforms) == len(set(platforms)), f"{component_id}: duplicate platform")
        findings.require(set(platforms) <= known_platforms, f"{component_id}: unknown platform")
        findings.require(entry.get("platform_status") in {"unassessed", "planned", "assessed", "unsupported"}, f"{component_id}: invalid platform status")
        graph[component_id] = [item for item in dependencies if item in set(component_ids)]
        for digest in entry.get("artifact_digests", []) + entry.get("evidence_hashes", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{component_id}: invalid digest {digest!r}")
        if entry.get("admission") == "admitted":
            findings.require(bool(entry.get("repository")), f"{component_id}: admitted component lacks repository")
            findings.require(bool(REVISION_RE.fullmatch(entry.get("revision", ""))), f"{component_id}: admitted component lacks immutable revision")
            findings.require(bool(entry.get("artifact_digests")), f"{component_id}: admitted component lacks artifact digest")
            findings.require(bool(entry.get("platforms")), f"{component_id}: admitted component lacks platform declaration")
            findings.require(entry.get("platform_status") == "assessed", f"{component_id}: admitted component platform state is not assessed")
            missing_admissions = [
                dependency
                for dependency in dependencies
                if records_by_id.get(dependency, {}).get("admission") != "admitted"
            ]
            findings.require(not missing_admissions, f"{component_id}: admitted component has non-admitted dependencies {missing_admissions}")
            findings.require(bool(REVISION_RE.fullmatch(entry.get("rollback_mate", ""))), f"{component_id}: admitted component lacks rollback mate")
            findings.require(bool(entry.get("evidence_hashes")), f"{component_id}: admitted component lacks evidence")
    cycle = find_dependency_cycle(graph)
    findings.require(not cycle, f"component dependency cycle: {' -> '.join(cycle)}")
    for entry in externals:
        dependency_id = entry.get("id", "<missing>")
        findings.require(bool(REVISION_RE.fullmatch(entry.get("revision", ""))), f"{dependency_id}: external revision is not immutable")
        findings.require(entry.get("admission") in {"not_admitted", "admitted", "rejected", "revoked"}, f"{dependency_id}: invalid admission")
    return catalog


# Complexity: time O(d + g), Omega(d), tight Theta(d + g) for dependencies d
# and gate names g; auxiliary space O(d + g) for indexes.
def validate_phase0(findings: Findings, catalog: dict[str, Any]) -> dict[str, Any]:
    phase0 = load_toml("governance/phase0.toml")
    dependencies = phase0.get("dependencies", [])
    external_by_id = {entry["id"]: entry for entry in catalog.get("external_dependencies", [])}
    findings.require({entry.get("id") for entry in dependencies} == set(external_by_id), "Phase 0 dependency set differs from component catalog")
    findings.require(phase0.get("minimum_dependency_grade") == "A", "Phase 0 minimum dependency grade must remain A")
    findings.require(phase0.get("status") in {"blocked", "passed"}, "Phase 0 has an invalid status")
    all_admitted = True
    for entry in dependencies:
        dependency_id = entry.get("id", "<missing>")
        required = set(entry.get("required_gates", []))
        passed = set(entry.get("passed_gates", []))
        findings.require(bool(required), f"{dependency_id}: Phase 0 required gate set is empty")
        findings.require(passed <= required, f"{dependency_id}: passed unknown Phase 0 gate")
        findings.require(entry.get("status") in {"blocked", "passed"}, f"{dependency_id}: invalid Phase 0 status")
        findings.require(entry.get("review") in {"not_started", "failed", "passed"}, f"{dependency_id}: invalid Phase 0 review state")
        findings.require(entry.get("admission") in {"not_admitted", "admitted", "rejected", "revoked"}, f"{dependency_id}: invalid Phase 0 admission")
        findings.require(entry.get("revision") == external_by_id.get(dependency_id, {}).get("revision"), f"{dependency_id}: Phase 0 revision differs from catalog")
        for digest in entry.get("evidence", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{dependency_id}: invalid Phase 0 evidence digest")
        admitted = entry.get("admission") == "admitted"
        catalog_admitted = external_by_id.get(dependency_id, {}).get("admission") == "admitted"
        if admitted:
            findings.require(catalog_admitted, f"{dependency_id}: Phase 0 admission outruns component catalog admission")
        grade = entry.get("grade")
        findings.require(grade in {"ungraded", "A", "A+"}, f"{dependency_id}: invalid Phase 0 grade")
        grade_evidence = entry.get("grade_evidence", [])
        grade_evidence_revision = entry.get("grade_evidence_revision", "")
        grade_reviewer = entry.get("grade_reviewer", "")
        grade_review = entry.get("grade_review")
        findings.require(isinstance(grade_evidence, list), f"{dependency_id}: Phase 0 grade evidence must be an array")
        for digest in grade_evidence:
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{dependency_id}: invalid Phase 0 grade evidence digest")
        findings.require(grade_review in {"not_started", "failed", "passed"}, f"{dependency_id}: invalid Phase 0 grade review state")
        grade_admitted = (
            grade in {"A", "A+"}
            and bool(grade_evidence)
            and grade_evidence_revision == entry.get("revision")
            and bool(grade_reviewer)
            and grade_reviewer != dependency_id
            and grade_review == "passed"
        )
        dependency_ready = admitted and catalog_admitted and grade_admitted and passed == required and bool(entry.get("evidence")) and entry.get("review") == "passed"
        findings.require((entry.get("status") == "passed") == dependency_ready, f"{dependency_id}: Phase 0 status does not match complete dependency admission state")
        all_admitted &= dependency_ready and entry.get("status") == "passed"
        if admitted:
            findings.require(grade in {"A", "A+"}, f"{dependency_id}: admitted Phase 0 dependency is below A grade")
            findings.require(bool(grade_evidence), f"{dependency_id}: admitted Phase 0 grade lacks evidence")
            findings.require(grade_evidence_revision == entry.get("revision"), f"{dependency_id}: Phase 0 grade evidence is not bound to the admitted revision")
            findings.require(bool(grade_reviewer) and grade_reviewer != dependency_id, f"{dependency_id}: Phase 0 grade lacks an independent reviewer")
            findings.require(grade_review == "passed", f"{dependency_id}: Phase 0 grade review has not passed")
            findings.require(not entry.get("gaps"), f"{dependency_id}: admitted dependency retains gaps")
    findings.require(phase0.get("applies_to_channels") == ["beta", "stable"], "Phase 0 channel scope drifted")
    findings.require(phase0.get("alpha_gate") == "BFW-ALPHA-0", "Phase 0 alpha-gate reference drifted")
    findings.require(bool(phase0.get("beta_stable_runtime_allowed")) == all_admitted, "Phase 0 beta/stable runtime flag does not match complete admission state")
    findings.require(bool(phase0.get("out_of_alpha_implementation_allowed")) == all_admitted, "Phase 0 out-of-alpha implementation flag does not match complete A-grade admission state")
    findings.require((phase0.get("status") == "passed") == all_admitted, "Phase 0 status does not match complete admission state")
    return phase0


# Complexity: time O(d + g), Omega(d), tight Theta(d + g) for dependencies d
# and safety/dependency gates g; auxiliary space O(d + g) for indexes.
def validate_alpha(findings: Findings, catalog: dict[str, Any]) -> dict[str, Any]:
    alpha = load_toml("governance/alpha.toml")
    dependencies = alpha.get("dependencies", [])
    external_by_id = {entry["id"]: entry for entry in catalog.get("external_dependencies", [])}
    findings.require({entry.get("id") for entry in dependencies} == set(external_by_id), "Alpha dependency set differs from component catalog")
    findings.require(alpha.get("gate_id") == "BFW-ALPHA-0", "Alpha gate identity drifted")
    findings.require(alpha.get("full_admission_gate") == "BFW-PHASE-0", "Alpha full-admission reference drifted")
    findings.require(alpha.get("platform") == "linux", "Alpha platform must remain Linux")
    findings.require(alpha.get("distribution") == "alpine", "Alpha distribution must remain Alpine")
    findings.require(alpha.get("architecture") == "x86_64", "Alpha architecture must remain x86_64")
    findings.require(alpha.get("runtime_contract") == "rpc-plugin-system-v2", "Alpha runtime contract must remain rpc-plugin-system v2")
    findings.require(alpha.get("source_implementation_phase0_exempt") is True, "Alpha source implementation must remain exempt from Phase 0")
    findings.require(alpha.get("offline_simulation_phase0_exempt") is True, "Alpha offline simulation must remain exempt from Phase 0")
    findings.require(alpha.get("workflow_activation_required") is True, "Alpha source work must require normal workflow activation")
    findings.require(alpha.get("production_allowed") is False, "Alpha must never authorize production")
    findings.require(alpha.get("status") in {"blocked", "passed"}, "Alpha has an invalid status")
    findings.require(alpha.get("review") in {"not_started", "failed", "passed"}, "Alpha has an invalid review state")
    findings.require(alpha.get("admission") in {"not_admitted", "alpha_admitted", "rejected", "revoked"}, "Alpha has an invalid admission")

    required_safety = set(alpha.get("required_safety_gates", []))
    passed_safety = set(alpha.get("passed_safety_gates", []))
    findings.require(bool(required_safety), "Alpha safety gate set is empty")
    findings.require(passed_safety <= required_safety, "Alpha passed an unknown safety gate")
    for digest in alpha.get("evidence", []):
        findings.require(bool(SHA256_RE.fullmatch(digest)), "Alpha has an invalid safety evidence digest")

    dependencies_ready = True
    for entry in dependencies:
        dependency_id = entry.get("id", "<missing>")
        required = set(entry.get("required_gates", []))
        passed = set(entry.get("passed_gates", []))
        findings.require(bool(required), f"{dependency_id}: Alpha required gate set is empty")
        findings.require(passed <= required, f"{dependency_id}: passed unknown Alpha gate")
        findings.require(entry.get("status") in {"blocked", "passed"}, f"{dependency_id}: invalid Alpha status")
        findings.require(entry.get("review") in {"not_started", "failed", "passed"}, f"{dependency_id}: invalid Alpha review state")
        findings.require(entry.get("admission") in {"not_admitted", "alpha_admitted", "rejected", "revoked"}, f"{dependency_id}: invalid Alpha admission")
        selected_version = entry.get("selected_version", "")
        revision = entry.get("revision", "")
        if dependency_id == "rpc-plugin-system":
            findings.require(entry.get("required_version") == "2.x", "rpc-plugin-system: Alpha required version must remain 2.x")
            if selected_version:
                findings.require(bool(re.fullmatch(r"2\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?", selected_version)), "rpc-plugin-system: Alpha selected version is not v2")
        if selected_version or revision:
            findings.require(bool(selected_version), f"{dependency_id}: Alpha version and revision must be selected together")
            findings.require(bool(REVISION_RE.fullmatch(revision)), f"{dependency_id}: Alpha revision is not immutable")
            findings.require(revision == external_by_id.get(dependency_id, {}).get("revision"), f"{dependency_id}: Alpha revision differs from catalog")
        for digest in entry.get("evidence", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{dependency_id}: invalid Alpha evidence digest")
        admitted = entry.get("admission") == "alpha_admitted"
        ready = admitted and bool(selected_version) and bool(REVISION_RE.fullmatch(revision)) and passed == required and bool(entry.get("evidence")) and entry.get("review") == "passed"
        findings.require((entry.get("status") == "passed") == ready, f"{dependency_id}: Alpha status does not match complete dependency admission state")
        dependencies_ready &= ready and entry.get("status") == "passed"
        if admitted:
            findings.require(not entry.get("gaps"), f"{dependency_id}: alpha-admitted dependency retains gaps")

    all_ready = dependencies_ready and passed_safety == required_safety and bool(alpha.get("evidence")) and alpha.get("review") == "passed"
    for field in ("host_network_mutation_allowed", "installer_disk_mutation_allowed", "alpha_distribution_allowed"):
        findings.require(bool(alpha.get(field)) == all_ready, f"Alpha {field} flag does not match complete minimum admission state")
    findings.require((alpha.get("status") == "passed") == all_ready, "Alpha status does not match complete minimum admission state")
    findings.require((alpha.get("admission") == "alpha_admitted") == all_ready, "Alpha admission does not match complete minimum admission state")
    return alpha


# Complexity: time O(c + e), Omega(c), tight Theta(c + e) for catalog entries c
# and dependency edges e; auxiliary space O(c).
def validate_release(findings: Findings, catalog: dict[str, Any], phase0: dict[str, Any], alpha: dict[str, Any]) -> dict[str, Any]:
    release = load_toml("governance/releases/v0.1.toml")
    catalog_by_id = {entry["id"]: entry for entry in catalog.get("components", [])}
    included = release.get("included", [])
    build_components = release.get("build_components", [])
    deferred = release.get("deferred", [])
    composition = release.get("composition", [])
    build_composition = release.get("build_composition", [])
    findings.require(release.get("alpha_gate") == "BFW-ALPHA-0", "v0.1 alpha gate drifted")
    findings.require(release.get("phase0_gate") == "BFW-PHASE-0", "v0.1 Phase 0 gate drifted")
    findings.require(release.get("phase0_required_for") == ["beta", "stable"], "v0.1 Phase 0 channel policy drifted")
    findings.require(release.get("release_manifest_schema") == "bfw.release/v1", "v0.1 release manifest schema drifted")
    channel = release.get("channel")
    findings.require(channel in {"design", "development", "alpha", "beta", "stable"}, "v0.1 release channel is invalid")
    findings.require(release.get("status") in {"profile_only", "blocked", "passed"}, "v0.1 release status is invalid")
    findings.require(release.get("admission") in {"not_admitted", "admitted", "rejected", "revoked"}, "v0.1 release admission is invalid")
    findings.require((release.get("status") == "passed") == (release.get("admission") == "admitted"), "v0.1 release status does not match admission state")
    if channel == "design":
        findings.require(release.get("status") == "profile_only" and release.get("admission") == "not_admitted", "v0.1 design profile cannot become an admitted release")
    findings.require(len(included) == len(set(included)), "v0.1 includes duplicate component")
    findings.require(len(build_components) == len(set(build_components)), "v0.1 repeats build component")
    findings.require(len(deferred) == len(set(deferred)), "v0.1 defers duplicate component")
    role_sets = [set(included), set(build_components), set(deferred)]
    findings.require(not any(left & right for index, left in enumerate(role_sets) for right in role_sets[index + 1 :]), "v0.1 runtime/build/deferred overlap")
    findings.require(set().union(*role_sets) == set(catalog_by_id), "v0.1 profile does not partition the complete component catalog")
    findings.require({entry.get("id") for entry in composition} == set(included), "v0.1 composition does not match included profile")
    findings.require({entry.get("id") for entry in build_composition} == set(build_components), "v0.1 build composition does not match build profile")
    for component_id in included:
        findings.require(catalog_by_id.get(component_id, {}).get("kind") != "distribution-component", f"v0.1 installs distribution component {component_id}")
    for component_id in build_components:
        findings.require(catalog_by_id.get(component_id, {}).get("kind") == "distribution-component", f"v0.1 build component is not a distribution component: {component_id}")
    for component_id in included:
        component = catalog_by_id.get(component_id, {})
        missing = [dependency for dependency in component.get("dependencies", []) if dependency in catalog_by_id and dependency not in included]
        findings.require(not missing, f"v0.1 dependency closure missing {component_id}: {missing}")
    build_available = set(included) | set(build_components)
    for component_id in build_components:
        component = catalog_by_id.get(component_id, {})
        missing = [dependency for dependency in component.get("dependencies", []) if dependency in catalog_by_id and dependency not in build_available]
        findings.require(not missing, f"v0.1 build dependency closure missing {component_id}: {missing}")
    for entry in composition + build_composition:
        component_id = entry.get("id", "<missing>")
        for digest in entry.get("artifact_digests", []) + entry.get("evidence_hashes", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"v0.1 {component_id}: invalid digest")
        if release.get("admission") == "admitted":
            findings.require(bool(REVISION_RE.fullmatch(entry.get("revision", ""))), f"v0.1 {component_id}: admitted composition lacks revision")
            findings.require(bool(entry.get("artifact_digests")), f"v0.1 {component_id}: admitted composition lacks artifacts")
            findings.require(bool(REVISION_RE.fullmatch(entry.get("rollback_mate", ""))), f"v0.1 {component_id}: admitted composition lacks rollback mate")
            findings.require(bool(entry.get("evidence_hashes")), f"v0.1 {component_id}: admitted composition lacks evidence")
    if release.get("admission") == "admitted" and channel == "alpha":
        findings.require(alpha.get("alpha_distribution_allowed") is True, "v0.1 alpha admission outruns BFW-ALPHA-0 distribution permission")
    if release.get("admission") == "admitted" and channel in release.get("phase0_required_for", []):
        findings.require(phase0.get("beta_stable_runtime_allowed") is True, "v0.1 beta/stable admission outruns complete BFW-PHASE-0 admission")
    findings.require(not (release.get("status") == "profile_only" and release.get("admission") == "admitted"), "profile-only v0.1 cannot be admitted")
    return release


# Complexity: time O(n), Omega(n), tight Theta(n) in traversed JSON nodes n;
# auxiliary space O(h + r) for recursion depth h and collected references r.
def collect_refs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                yield child
            yield from collect_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from collect_refs(child)


# Complexity: worst-case time O(n * b) for n visited schema/instance nodes and
# combinator branching b; Omega(n), with tight Theta(n) when no combinators
# branch. Auxiliary space O(h + n) for recursion depth h and error paths.
def schema_instance_errors(
    schema: dict[str, Any],
    instance: Any,
    schema_dir: pathlib.Path,
    path: str = "$",
    document_schema: dict[str, Any] | None = None,
) -> list[str]:
    """Validate the fail-closed JSON Schema subset used by Bifrost fixtures."""
    if document_schema is None:
        document_schema = schema
    errors: list[str] = []
    if "$ref" in schema:
        reference = str(schema["$ref"])
        target_name, _, fragment = reference.partition("#")
        target_document = load_json(schema_dir / target_name) if target_name else document_schema
        target = target_document
        if fragment:
            for token in fragment.lstrip("/").split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                target = target[token]
        errors.extend(
            schema_instance_errors(
                target,
                instance,
                schema_dir,
                path,
                target_document,
            )
        )

    expected = schema.get("type")
    expected_types = [expected] if isinstance(expected, str) else expected
    type_checks = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": lambda value: isinstance(value, bool),
        "null": lambda value: value is None,
    }
    if expected_types and not any(type_checks[item](instance) for item in expected_types):
        return errors + [f"{path}: expected type {expected_types}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value differs from const")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value is not in enum")

    if isinstance(instance, dict):
        required = set(schema.get("required", []))
        for key in sorted(required - set(instance)):
            errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(schema_instance_errors(properties[key], value, schema_dir, f"{path}.{key}", document_schema))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unknown property {key}")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: too many items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in instance}) != len(instance):
            errors.append(f"{path}: duplicate array item")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(schema_instance_errors(item_schema, value, schema_dir, f"{path}[{index}]", document_schema))
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: string is too long")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: string does not match pattern")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(instance.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{path}: invalid date-time")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")

    for child in schema.get("allOf", []):
        errors.extend(schema_instance_errors(child, instance, schema_dir, path, document_schema))
    if "anyOf" in schema:
        branches = [schema_instance_errors(child, instance, schema_dir, path, document_schema) for child in schema["anyOf"]]
        if all(branch for branch in branches):
            errors.append(f"{path}: no anyOf branch matched")
    if "if" in schema:
        condition_matches = not schema_instance_errors(schema["if"], instance, schema_dir, path, document_schema)
        selected = schema.get("then" if condition_matches else "else")
        if isinstance(selected, dict):
            errors.extend(schema_instance_errors(selected, instance, schema_dir, path, document_schema))
    return errors


# Complexity: time O(s + n + f * v), Omega(s), where s is schema files, n is
# schema nodes, f is fixtures, and v is validation work; auxiliary O(s + n).
def validate_schemas(findings: Findings) -> None:
    expected = {
        "audit-event.schema.json", "canonical-config.schema.json",
        "capability.schema.json", "common.schema.json",
        "compatibility.schema.json", "deployment-profile.schema.json",
        "fabric-plan.schema.json", "goka-plan.schema.json",
        "ha-deployment-profile.schema.json", "health.schema.json", "ids-plan.schema.json",
        "kubernetes-ha-profile.schema.json", "plan.schema.json",
        "plugin-manifest.schema.json", "release.schema.json",
        "rollback-record.schema.json", "transaction.schema.json",
        "switch-plan.schema.json", "ui-manifest.schema.json",
    }
    schema_dir = ROOT / "schemas/v1"
    paths = sorted(schema_dir.glob("*.json"))
    findings.require({path.name for path in paths} == expected, "versioned schema set is incomplete or unexpected")
    identifiers: set[str] = set()
    for path in paths:
        try:
            schema = load_json(path)
        except (OSError, json.JSONDecodeError) as error:
            findings.add(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
            continue
        findings.require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{path.name}: wrong JSON Schema dialect")
        identifier = schema.get("$id", "")
        findings.require(bool(identifier) and identifier not in identifiers, f"{path.name}: missing or duplicate $id")
        identifiers.add(identifier)
        if path.name != "common.schema.json":
            findings.require(schema.get("type") == "object", f"{path.name}: top level must be object")
            findings.require(schema.get("additionalProperties") is False, f"{path.name}: top-level unknown properties must fail closed")
        for reference in collect_refs(schema):
            target = reference.split("#", 1)[0]
            if target and not target.startswith(("http://", "https://")):
                findings.require((path.parent / target).is_file(), f"{path.name}: missing local $ref target {target}")
    fixture_dir = schema_dir / "fixtures"
    fixture_paths = sorted(fixture_dir.glob("*.json"))
    expected_fixtures = {
        "deployment-profile.invalid.json", "deployment-profile.valid.json",
        "fabric-plan.invalid.json", "fabric-plan.valid.json",
        "goka-plan.invalid.json", "goka-plan.valid.json",
        "ha-deployment-profile.invalid.json", "ha-deployment-profile.valid.json",
        "ids-plan.invalid.json", "ids-plan.valid.json",
        "kubernetes-ha-profile.invalid.json", "kubernetes-ha-profile.valid.json",
        "release.invalid.json", "release.valid.json",
        "switch-plan.invalid.json", "switch-plan.valid.json",
    }
    findings.require({path.name for path in fixture_paths} == expected_fixtures, "representative schema fixture set is incomplete or unexpected")
    for path in fixture_paths:
        fixture = load_json(path)
        schema_name = fixture.get("schema_file")
        expected_valid = fixture.get("valid")
        findings.require(schema_name in expected, f"{path.name}: unknown target schema")
        findings.require(isinstance(expected_valid, bool), f"{path.name}: valid must be boolean")
        if schema_name in expected and isinstance(expected_valid, bool):
            errors = schema_instance_errors(load_json(schema_dir / schema_name), fixture.get("instance"), schema_dir)
            findings.require((not errors) == expected_valid, f"{path.name}: fixture expectation mismatch: {errors[:3]}")


# Complexity: time O(p + c + e), Omega(p + c), tight Theta(p + c + e) for
# profiles p, catalog/release components c, and declared effects e; auxiliary
# space O(p + c + e) for indexes and uniqueness checks.
def validate_deployment_profiles(findings: Findings) -> None:
    policy = load_toml("governance/deployment-profiles.toml")
    profiles = policy.get("profiles", [])
    by_id = {entry.get("id"): entry for entry in profiles}
    findings.require(len(profiles) == len(by_id), "duplicate deployment profile ID")
    findings.require(set(by_id) == {"router", "switch", "converged"}, "deployment profile set is incomplete or unexpected")
    findings.require(policy.get("default_profile") in by_id, "default deployment profile is unknown")
    findings.require(policy.get("management_address_is_transit") is False, "management address must not imply transit forwarding")
    findings.require(set(policy.get("product_scopes", [])) == {"standalone", "fabric"}, "product deployment scopes are incomplete")
    findings.require(policy.get("v0_1_scopes") == ["standalone"], "v0.1 must keep fabric scope deferred")
    catalog = load_toml("governance/components.toml")
    known = {entry.get("id") for entry in catalog.get("components", [])}
    release = load_toml("governance/releases/v0.1.toml")
    included = set(release.get("included", []))
    required_fields = {"id", "description", "required_components", "data_plane_layers", "enabled_effects", "denied_effects", "transition_policy"}
    for profile_id, profile in by_id.items():
        findings.require(required_fields <= set(profile), f"{profile_id}: incomplete deployment profile")
        required = profile.get("required_components", [])
        layers = profile.get("data_plane_layers", [])
        enabled = profile.get("enabled_effects", [])
        denied = profile.get("denied_effects", [])
        findings.require(len(required) == len(set(required)), f"{profile_id}: duplicate required component")
        findings.require(len(layers) == len(set(layers)), f"{profile_id}: duplicate data-plane layer")
        findings.require(set(layers) <= {2, 3, 4}, f"{profile_id}: unknown data-plane layer")
        findings.require(len(enabled) == len(set(enabled)), f"{profile_id}: duplicate enabled effect")
        findings.require(len(denied) == len(set(denied)), f"{profile_id}: duplicate denied effect")
        findings.require(set(required) <= known, f"{profile_id}: unknown required component")
        findings.require(set(required) <= included, f"{profile_id}: v0.1 lacks required profile component")
        findings.require(not (set(enabled) & set(denied)), f"{profile_id}: effect is both enabled and denied")
        findings.require(profile.get("transition_policy") == "commit-confirmed", f"{profile_id}: unsafe role transition policy")
    findings.require("user-layer2-bridge-forwarding" in by_id.get("router", {}).get("denied_effects", []), "router profile does not deny user Layer-2 switching")
    findings.require({"wan-edge-routing", "nat", "stateful-transport-policy"} <= set(by_id.get("switch", {}).get("denied_effects", [])), "switch profile does not bound Layer-3 switching from edge/Layer-4 effects")
    findings.require({"layer2-switching", "layer3-switching", "layer3-routing", "stateful-transport-policy", "packet-filter"} <= set(by_id.get("converged", {}).get("enabled_effects", [])), "converged profile lacks required forwarding effects")
    findings.require(not by_id.get("converged", {}).get("denied_effects", []), "converged profile unexpectedly denies an admitted domain")
    expected_components = {
        "router": {"bfw-core", "bfw-network", "bfw-routing", "bfw-firewall"},
        "switch": {"bfw-core", "bfw-network", "bfw-switching", "bfw-routing"},
        "converged": {"bfw-core", "bfw-network", "bfw-switching", "bfw-routing", "bfw-firewall"},
    }
    for profile_id, expected in expected_components.items():
        findings.require(set(by_id.get(profile_id, {}).get("required_components", [])) == expected, f"{profile_id}: required component closure drifted")
        findings.require("management-termination" in by_id.get(profile_id, {}).get("enabled_effects", []), f"{profile_id}: shared management termination is missing")
    expected_layers = {"router": {3, 4}, "switch": {2, 3}, "converged": {2, 3, 4}}
    for profile_id, expected in expected_layers.items():
        findings.require(set(by_id.get(profile_id, {}).get("data_plane_layers", [])) == expected, f"{profile_id}: data-plane layer declaration drifted")


# Complexity: time O(p), Omega(p), tight Theta(p) for controller profiles p;
# auxiliary space O(p) for the profile index.
def validate_kubernetes_ha(findings: Findings) -> None:
    policy = load_toml("governance/kubernetes-ha.toml")
    profiles = policy.get("profiles", [])
    by_id = {entry.get("id"): entry for entry in profiles}
    findings.require(set(by_id) == {"single-controller", "ha-controller"}, "Kubernetes HA profile set is incomplete")
    findings.require(policy.get("status") == "planned", "Kubernetes HA must remain a first-party planned profile")
    findings.require(policy.get("managed_node_mode") == "native-agent", "managed nodes must use native agents")
    findings.require(policy.get("forwarding_dependency") == "autonomous-last-known-good", "Kubernetes must not own forwarding availability")
    findings.require(policy.get("control_loss_policy") == "freeze-mutations-retain-forwarding", "unsafe Kubernetes control-loss policy")
    findings.require(policy.get("worker_membership_required") is False, "managed nodes must not require Kubernetes worker membership")
    single = by_id.get("single-controller", {})
    findings.require(single.get("ha") is False and single.get("minimum_controllers") == 1, "single-controller profile misstates HA")
    findings.require(single.get("availability_claim") == "management-single-point-of-failure", "single-controller availability is overstated")
    ha = by_id.get("ha-controller", {})
    minimum = ha.get("minimum_controllers", 0)
    findings.require(ha.get("ha") is True and minimum >= 3 and minimum % 2 == 1, "HA controller count must be odd and at least three")
    findings.require(ha.get("odd_controller_count_required") is True, "HA profile does not require odd controller count")
    findings.require(ha.get("minimum_failure_domains", 0) >= 3, "HA profile lacks three failure domains")
    findings.require(ha.get("consensus") == "quorum", "HA profile lacks quorum consensus")


# Complexity: time O(p + h + o), Omega(p + h + o), tight Theta(p + h + o)
# for protocol, health, and owner declarations; auxiliary space O(p + h + o).
def validate_goka(findings: Findings) -> None:
    policy = load_toml("governance/goka.toml")
    findings.require(policy.get("product_name") == "GoKA", "GoKA product name drifted")
    findings.require(policy.get("component") == "bfw-ha", "GoKA component binding drifted")
    findings.require(policy.get("status") == "deferred", "GoKA must remain deferred")
    findings.require(policy.get("implementation_language") == "Go", "GoKA implementation language drifted")
    findings.require(policy.get("clean_room") is True, "GoKA must remain clean-room")
    denied = ("keepalived_source_allowed", "keepalived_library_allowed", "keepalived_binary_allowed", "keepalived_runtime_allowed", "keepalived_configuration_authority", "arbitrary_shell_health_allowed")
    findings.require(all(policy.get(field) is False for field in denied), "GoKA permits forbidden Keepalived or shell authority")
    findings.require(set(policy.get("protocols", [])) == {"vrrp-v2-ipv4", "vrrp-v3-ipv4", "vrrp-v3-ipv6"}, "GoKA protocol set drifted")
    findings.require(set(policy.get("peer_modes", [])) == {"multicast", "unicast"}, "GoKA peer modes drifted")
    findings.require("platform-adapter" in policy.get("effect_owners", []), "GoKA lacks typed platform effect owner")
    findings.require(policy.get("keepalived_import") == "exact-versioned-subset-hard-reject", "unsafe Keepalived import policy")


# Complexity: time O(p), Omega(p), tight Theta(p) for HA profiles p;
# auxiliary space O(p) for the profile index.
def validate_ha_profiles(findings: Findings) -> None:
    policy = load_toml("governance/ha-profiles.toml")
    expected = {"goka-native", "kubernetes-managed"}
    findings.require(set(policy.get("profiles", [])) == expected, "out-of-box HA profiles are not exactly GoKA and Kubernetes")
    contracts = policy.get("profile_contracts", [])
    by_id = {entry.get("id"): entry for entry in contracts}
    findings.require(set(by_id) == expected and len(contracts) == 2, "HA profile contracts are incomplete or duplicated")
    findings.require(policy.get("simultaneous_management_coordinators_allowed") is False, "HA profiles permit competing coordinators")
    findings.require(policy.get("canonical_authority") == "bfw-core", "HA profile canonical authority drifted")
    findings.require(policy.get("fast_failover_authority") == "native-node", "HA profile fast failover is not node-local")
    goka = by_id.get("goka-native", {})
    findings.require(goka.get("management_coordinator") == "goka" and goka.get("external_controller_substrate_required") is False, "GoKA-native profile contract drifted")
    kubernetes = by_id.get("kubernetes-managed", {})
    findings.require(kubernetes.get("management_coordinator") == "kubernetes" and kubernetes.get("external_controller_substrate_required") is True, "Kubernetes-managed profile contract drifted")
    for profile_id, contract in by_id.items():
        findings.require(contract.get("first_party") is True and contract.get("packaged_out_of_box") is True, f"{profile_id}: not first-party out-of-box")
        findings.require(contract.get("status") == "planned", f"{profile_id}: unexpected profile status")


# Complexity: time O(a + t + n), Omega(a + t), tight Theta(a + t + n) for ADRs
# a, templates t, and their bytes n; auxiliary space O(a + t).
def validate_adrs_and_templates(findings: Findings) -> None:
    adr_dir = ROOT / "documents/adrs"
    adr_paths = sorted(path for path in adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md") if path.name != "0000-template.md")
    findings.require(len(adr_paths) == 16, "expected sixteen settled ADRs")
    index = (adr_dir / "README.md").read_text(encoding="utf-8")
    for path in adr_paths:
        text = path.read_text(encoding="utf-8")
        number = path.name[:4]
        findings.require(f"ADR-{number}" in text, f"{path.name}: ADR id mismatch")
        findings.require(f"({path.name})" in index, f"{path.name}: missing from ADR index")
        findings.require("Status: Accepted" in text, f"{path.name}: settled ADR is not accepted")
        for section in ("## Context", "## Decision", "## Consequences", "## Alternatives considered", "## Verification"):
            findings.require(section in text, f"{path.name}: missing {section}")
        findings.require("{{" not in text, f"{path.name}: accepted ADR contains placeholder")

    required_templates = {
        "README.md", "TEST-PLAN.md", "compatibility.toml", "evidence.toml",
        "release.toml", "INDEPENDENT-REVIEW.md", "documents/PRD.md",
        "documents/ARCHITECTURE.md", "documents/IMPLEMENTATION-SPEC.md",
        "documents/THREAT-MODEL.md",
    }
    template_root = ROOT / "templates/component"
    actual = {str(path.relative_to(template_root)) for path in template_root.rglob("*") if path.is_file()}
    findings.require(actual == required_templates, "component template set is incomplete or unexpected")
    for relative in required_templates - {"README.md"}:
        text = (template_root / relative).read_text(encoding="utf-8")
        findings.require("{{" in text, f"template {relative} contains no explicit placeholders")
        if relative.endswith(".toml"):
            try:
                with (template_root / relative).open("rb") as handle:
                    tomllib.load(handle)
            except tomllib.TOMLDecodeError as error:
                findings.add(f"template {relative} is invalid TOML: {error}")


# Complexity: time O(t + r + s), Omega(t + r + s), tight Theta(t + r + s)
# for targets t, roles r, and scenarios s; auxiliary space O(t + s).
def validate_test_lab(findings: Findings) -> None:
    lab = load_toml("governance/test-lab.toml")
    targets = lab.get("targets", [])
    findings.require({entry.get("platform") for entry in targets} == {"linux", "freebsd", "windows"}, "test lab platform target set is incomplete")
    for target in targets:
        status = target.get("status")
        if status == "pinned":
            findings.require(bool(target.get("os_release")), f"{target.get('id')}: pinned target lacks OS release")
            findings.require(bool(target.get("kernel_or_runtime")), f"{target.get('id')}: pinned target lacks runtime")
            findings.require(bool(SHA256_RE.fullmatch(target.get("image_digest", ""))), f"{target.get('id')}: pinned target lacks image digest")
        else:
            findings.require(status == "unpinned", f"{target.get('id')}: invalid target status")
            findings.require(not target.get("image_digest"), f"{target.get('id')}: unpinned target carries misleading digest")
    required_scenarios = {"upgrade", "interrupted-upgrade", "last-known-good-rollback", "local-console-recovery", "packet-policy-oracle", "ha-failover", "split-brain", "secret-redaction", "switch-access-trunk-vlan-isolation", "switch-layer2-loop-stp-convergence", "switch-lacp-member-loss", "switch-fdb-learning-aging-static", "switch-storm-control", "switch-multicast-snooping", "switch-management-path-rollback", "switch-offload-parity", "role-router-only", "role-switch-only", "role-converged", "role-transition-rollback", "switch-management-address-non-transit", "switch-layer3-svi-inter-vlan", "switch-layer3-routed-port", "switch-local-fabric-versus-edge-denial", "router-layer4-state-policy", "router-nat-port-forward", "layer4-no-layer7-authority", "ids-passive-observation", "ids-inline-fail-open", "ids-inline-fail-closed", "ids-fragment-stream-evasion", "ids-rule-dialect-rejection", "ids-overload-loss-accounting", "ids-alert-evidence-redaction", "ids-enforcement-authority-denial", "ids-ruleset-rollback"}
    required_scenarios |= {"fabric-membership-quorum-fencing", "fabric-asymmetric-partition", "fabric-evpn-vxlan-mobility", "fabric-vrf-anycast-ecmp", "fabric-distributed-firewall-placement", "fabric-state-owner-failover", "fabric-mtu-bum-offload", "fabric-staged-upgrade-rollback", "fabric-scale-convergence"}
    required_scenarios |= {"kubernetes-single-controller-loss", "kubernetes-controller-quorum-loss", "kubernetes-total-control-plane-loss", "kubernetes-api-etcd-cni-storage-loss", "kubernetes-management-partition", "kubernetes-stale-plan-replay", "kubernetes-autonomous-forwarding", "kubernetes-controller-rebuild", "kubernetes-rolling-upgrade-rollback", "kubernetes-rbac-secret-isolation"}
    required_scenarios |= {"goka-clean-room-provenance", "goka-vrrp-v2-v3-interop", "goka-malformed-packet-fuzz", "goka-timer-election-preemption", "goka-split-brain-duplicate-owner", "goka-health-shell-denial", "goka-keepalived-import-rejection", "goka-platform-parity", "goka-restart-upgrade-rollback", "goka-performance-boundaries"}
    required_scenarios |= {"ha-profile-exact-two-packaged", "ha-profile-shared-contract-parity", "ha-profile-competing-coordinator-denial", "ha-profile-cross-migration", "ha-profile-migration-interruption-rollback", "ha-profile-release-composition"}
    required_scenarios |= {"alpha-install-boot-reset", "alpha-basic-router-path", "alpha-basic-switch-path", "alpha-unknown-state-recovery", "alpha-channel-promotion-denial", "alpha-effect-gate-denial"}
    findings.require(required_scenarios <= set(lab.get("required_scenarios", [])), "test lab lacks required scenario classes")
    role_counts = {entry.get("id"): entry.get("count", 0) for entry in lab.get("roles", [])}
    findings.require(role_counts.get("ha-node", 0) >= 2, "test lab needs two HA nodes")
    findings.require(role_counts.get("traffic-generator", 0) >= 2, "test lab needs independent traffic endpoints")
    findings.require(role_counts.get("switch-port", 0) >= 4, "test lab needs four independent switch-port fixtures")
    findings.require(role_counts.get("fabric-node", 0) >= 3, "test lab needs three distributed fabric nodes")
    findings.require(role_counts.get("kubernetes-controller", 0) >= 3, "test lab needs three Kubernetes controller members")


# Complexity: time O(f + n), Omega(f), tight Theta(f + n) for files f and
# scanned bytes n; auxiliary space O(f) for path inventory.
def validate_repository_boundary(findings: Findings) -> None:
    forbidden_suffixes = {".go", ".rs", ".c", ".cc", ".cpp", ".h", ".java", ".ts", ".tsx", ".js", ".jsx", ".wasm", ".exe", ".dll", ".so", ".sh"}
    forbidden_names = {"go.mod", "Cargo.toml", "package.json"}
    paths = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    for path in paths:
        relative = path.relative_to(ROOT)
        findings.require(path.name not in forbidden_names, f"product runtime/build manifest forbidden in meta repo: {relative}")
        findings.require(path.suffix not in forbidden_suffixes, f"product runtime source/artifact forbidden in meta repo: {relative}")
        if path.suffix == ".py":
            findings.require(relative.parts[0] == "tools", f"Python is allowed only for governance tooling: {relative}")
        if path.suffix == ".sh":
            findings.require(relative.parts[0] == "tools", f"Shell is allowed only for governance tooling: {relative}")
    canonical = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in ("README.md", "documents/PRD.md", "documents/ARCHITECTURE.md", "documents/IMPLEMENTATION-SPEC.md"))
    findings.require("BFR-PRD-" not in canonical, "retired BFR requirement namespace found")
    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"(?i)\b(?:password|passwd|secret|token|api[_-]?key|private[_-]?key)\s*[:=]\s*[\"'][^\"'{<][^\"']{7,}[\"']"),
    )
    for path in paths:
        if path.suffix not in {".md", ".toml", ".json", ".yml", ".yaml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in secret_patterns:
            findings.require(not pattern.search(text), f"suspected secret material in {path.relative_to(ROOT)}")


# Complexity: time O(n), Omega(n), tight Theta(n) in workflow bytes n;
# auxiliary space O(n) for loaded text.
def validate_ci(findings: Findings) -> None:
    path = ROOT / ".forgejo/workflows/governance.yml"
    text = path.read_text(encoding="utf-8")
    findings.require("python3 tools/governance.py validate" in text, "CI does not run governance validation")
    findings.require("python3 tools/governance.py render --check" in text, "CI does not check generated views")
    findings.require("python3 -m unittest discover -s tools/tests -v" in text, "CI does not test governance tooling")
    findings.require("git diff --check HEAD^ HEAD" in text, "CI does not check committed patch whitespace")
    action_refs = re.findall(r"uses:\s*[^@\s]+@([^\s]+)", text)
    findings.require(bool(action_refs), "CI has no pinned action reference")
    for reference in action_refs:
        findings.require(bool(REVISION_RE.fullmatch(reference)), f"CI action is not pinned to an immutable commit: {reference}")


# Complexity: time O(n + e), Omega(n + e), tight Theta(n + e) in workflow
# TOML, feature, coverage, and event bytes; auxiliary space O(n + e) for
# indexes, graph state, and parsed events.
def validate_workflow(findings: Findings) -> dict[str, Any]:
    workflow = load_toml("workflow.toml")
    allowed_top_level = {
        "schema_version", "project", "profile", "authority", "active",
        "policy", "coverage", "features", "coverage_subsystems",
    }
    findings.require(set(workflow) <= allowed_top_level, "workflow has unknown top-level fields")
    findings.require(workflow.get("schema_version") == 2, "workflow schema version is unsupported")
    findings.require(workflow.get("project") == "Bifrost", "workflow project identity drifted")
    findings.require(workflow.get("profile") == "strict", "workflow profile must remain strict")
    findings.require(workflow.get("authority") == "workflow.toml", "workflow authority drifted")

    policy = workflow.get("policy", {})
    findings.require(policy.get("version") == 1, "workflow policy version is unsupported")
    findings.require(policy.get("one_active_feature") is True, "workflow must enforce one active feature")
    findings.require(policy.get("require_done_evidence") is True, "workflow must require done evidence")
    findings.require(policy.get("require_independent_review") is True, "workflow must require independent review")
    findings.require(policy.get("runtime_code_allowed") is False, "meta workflow unexpectedly allows runtime code")
    findings.require(policy.get("external_actions_allowed") is False, "meta workflow unexpectedly allows external actions")
    allowed_effects = set(policy.get("allowed_effects", []))
    findings.require(allowed_effects == {"read_only", "local_write"}, "meta workflow effect policy drifted")
    findings.require(policy.get("event_log") == "workflow.events.jsonl", "workflow event-log path drifted")
    findings.require(policy.get("workflow_root") == "workflow/features", "workflow root path drifted")

    features = workflow.get("features", [])
    feature_ids = [entry.get("id") for entry in features]
    feature_by_id = {entry.get("id"): entry for entry in features}
    findings.require(bool(features), "workflow feature registry is empty")
    findings.require(len(feature_ids) == len(set(feature_ids)), "workflow contains duplicate feature IDs")
    active_id = workflow.get("active")
    findings.require(active_id in feature_by_id, "workflow active feature is not registered")
    registry_ids = set(load_toml("governance/requirements.toml").get("requirements", {}))
    required_fields = {
        "id", "title", "state", "phase", "risk", "path", "requirements",
        "dependencies", "review", "evidence", "blockers", "allowed_effects",
        "acceptance",
    }
    allowed_states = {"planned", "ready", "in_progress", "blocked", "deferred", "failed", "done", "canceled", "split_required"}
    allowed_reviews = {"pending", "changes_requested", "approved", "rejected", "not_required"}
    allowed_risks = {"low", "medium", "high", "critical"}
    dependency_graph: dict[str, list[str]] = {}
    in_progress: list[str] = []
    all_feature_evidence: set[str] = set()
    for entry in features:
        feature_id = entry.get("id", "<missing>")
        findings.require(required_fields <= set(entry), f"{feature_id}: incomplete workflow feature record")
        findings.require(entry.get("state") in allowed_states, f"{feature_id}: invalid workflow feature state")
        findings.require(entry.get("review") in allowed_reviews, f"{feature_id}: invalid workflow review state")
        findings.require(entry.get("risk") in allowed_risks, f"{feature_id}: invalid workflow risk")
        path = entry.get("path", "")
        findings.require(path == f"workflow/features/{feature_id}", f"{feature_id}: workflow path is not canonical")
        feature_path = ROOT / path
        findings.require(feature_path.is_dir(), f"{feature_id}: workflow directory is missing")
        readme_path = feature_path / "README.md"
        findings.require(readme_path.is_file(), f"{feature_id}: workflow README is missing")
        if readme_path.is_file():
            readme = readme_path.read_text(encoding="utf-8")
            findings.require(not re.search(r"^Status:\s", readme, re.MULTILINE), f"{feature_id}: README duplicates canonical workflow state")
        requirements = entry.get("requirements", [])
        dependencies = entry.get("dependencies", [])
        evidence = entry.get("evidence", [])
        blockers = entry.get("blockers", [])
        state = entry.get("state")
        plan = entry.get("plan", "")
        findings.require(bool(requirements), f"{feature_id}: workflow requirement scope is empty")
        findings.require(len(requirements) == len(set(requirements)), f"{feature_id}: workflow requirement scope contains duplicates")
        findings.require(set(requirements) <= registry_ids, f"{feature_id}: workflow references unknown requirements")
        findings.require(len(dependencies) == len(set(dependencies)), f"{feature_id}: duplicate workflow dependency")
        findings.require(set(dependencies) <= set(feature_ids), f"{feature_id}: unknown workflow dependency")
        findings.require(feature_id not in dependencies, f"{feature_id}: workflow self dependency")
        findings.require(set(entry.get("allowed_effects", [])) <= allowed_effects, f"{feature_id}: workflow effect exceeds policy")
        findings.require(bool(entry.get("acceptance")), f"{feature_id}: workflow acceptance criteria are empty")
        if state in {"planned", "ready", "in_progress", "blocked"}:
            findings.require(bool(plan), f"{feature_id}: unfinished workflow lacks a checked plan")
            plan_path = ROOT / str(plan)
            findings.require(plan_path.parent == feature_path, f"{feature_id}: workflow plan must remain inside its feature directory")
            findings.require(plan_path.is_file(), f"{feature_id}: workflow plan is missing")
        for digest in evidence:
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{feature_id}: invalid workflow evidence digest")
        all_feature_evidence.update(evidence)
        dependency_graph[str(feature_id)] = [str(item) for item in dependencies]
        if state == "in_progress":
            in_progress.append(str(feature_id))
            findings.require(entry.get("review") in {"pending", "changes_requested"}, f"{feature_id}: active workflow review state is dishonest")
            findings.require(bool(blockers), f"{feature_id}: active workflow lacks explicit blockers or next gates")
            findings.require(all(feature_by_id[item].get("state") == "done" for item in dependencies), f"{feature_id}: active workflow has incomplete dependencies")
        if state == "done":
            findings.require(entry.get("review") == "approved", f"{feature_id}: done workflow lacks approved review")
            findings.require(bool(evidence), f"{feature_id}: done workflow lacks evidence")
            findings.require(not blockers, f"{feature_id}: done workflow retains blockers")
            evidence_path = feature_path / "evidence/verification.toml"
            findings.require(evidence_path.is_file(), f"{feature_id}: done workflow evidence file is missing")
            if evidence_path.is_file():
                findings.require(sha256_file(evidence_path) in evidence, f"{feature_id}: workflow evidence digest does not match verification record")
            reviews = list((feature_path / "review").glob("*.md"))
            findings.require(len(reviews) >= 2, f"{feature_id}: done workflow lacks two independent review records")
        if state in {"planned", "ready"}:
            findings.require(not evidence, f"{feature_id}: unstarted workflow carries completion evidence")
            findings.require(entry.get("review") == "pending", f"{feature_id}: unstarted workflow review must remain pending")
    findings.require(in_progress == [active_id], "workflow must have exactly one registered active feature")
    cycle = find_dependency_cycle(dependency_graph)
    findings.require(not cycle, f"workflow dependency cycle: {' -> '.join(cycle)}")

    folder_ids = {path.parent.name for path in (ROOT / "workflow/features").glob("*/README.md")}
    findings.require(folder_ids == set(feature_ids), "workflow folders and manifest feature IDs differ")

    coverage = workflow.get("coverage", {})
    findings.require(coverage.get("map") == "workflow/COVERAGE.md", "workflow coverage-map path drifted")
    findings.require(coverage.get("block_unresolved_high_risk") is True, "workflow must block unresolved high-risk coverage")
    coverage_entries = workflow.get("coverage_subsystems", [])
    coverage_ids = [entry.get("id") for entry in coverage_entries]
    findings.require(bool(coverage_entries), "workflow global coverage registry is empty")
    findings.require(len(coverage_ids) == len(set(coverage_ids)), "workflow contains duplicate coverage subsystem IDs")
    for entry in coverage_entries:
        subsystem_id = entry.get("id", "<missing>")
        findings.require(entry.get("risk") in allowed_risks, f"{subsystem_id}: invalid coverage risk")
        findings.require(bool(entry.get("owner")), f"{subsystem_id}: coverage owner is missing")
        findings.require(bool(entry.get("scope")), f"{subsystem_id}: coverage scope is empty")
        findings.require(bool(entry.get("required_harness")), f"{subsystem_id}: required coverage harness is empty")
        findings.require(isinstance(entry.get("known_gaps"), list), f"{subsystem_id}: coverage gaps must be an array")
        findings.require(bool(entry.get("next_increment")), f"{subsystem_id}: next coverage increment is missing")
        for digest in entry.get("evidence", []):
            findings.require(bool(SHA256_RE.fullmatch(digest)), f"{subsystem_id}: invalid coverage evidence digest")
            findings.require(digest in all_feature_evidence, f"{subsystem_id}: coverage evidence is not owned by a workflow feature")
        if entry.get("risk") in {"high", "critical"} and not entry.get("evidence"):
            findings.require(bool(entry.get("known_gaps")), f"{subsystem_id}: unresolved high-risk coverage lacks explicit gaps")
            plan = pathlib.Path(str(entry.get("plan", "")))
            findings.require(bool(entry.get("plan")), f"{subsystem_id}: unresolved high-risk coverage lacks a checked plan")
            findings.require(plan.parts[:1] == ("workflow",) and ".." not in plan.parts, f"{subsystem_id}: coverage plan path escapes workflow")
            findings.require((ROOT / plan).is_file(), f"{subsystem_id}: coverage plan is missing")

    event_path = ROOT / str(policy.get("event_log"))
    events = []
    for line_number, line in enumerate(event_path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            findings.add(f"workflow.events.jsonl:{line_number}: invalid JSON: {error}")
    findings.require(bool(events), "workflow event log is empty")
    findings.require(all(event.get("feature") in set(feature_ids) for event in events), "workflow event references unknown feature")
    parsed_times: list[datetime] = []
    states: dict[str, str] = {}
    globally_active: str | None = None
    for index, event in enumerate(events, start=1):
        try:
            parsed_times.append(datetime.fromisoformat(str(event.get("time"))))
        except ValueError:
            findings.add(f"workflow.events.jsonl:{index}: invalid ISO-8601 time")
            continue
        feature = str(event.get("feature"))
        old_state = str(event.get("from"))
        new_state = str(event.get("to"))
        expected_old = states.get(feature, "absent")
        findings.require(old_state == expected_old, f"workflow event {index}: illegal {feature} transition from {old_state}; expected {expected_old}")
        findings.require((old_state, new_state) in {("absent", "active"), ("active", "completed")}, f"workflow event {index}: unsupported state transition")
        if new_state == "active":
            findings.require(globally_active is None, f"workflow event {index}: {feature} overlaps active feature {globally_active}")
            globally_active = feature
        elif new_state == "completed":
            findings.require(globally_active == feature, f"workflow event {index}: {feature} completed while {globally_active} was active")
            evidence_path = ROOT / "workflow/features" / feature / "evidence/verification.toml"
            findings.require(evidence_path.is_file(), f"workflow event {index}: completion evidence is missing")
            if evidence_path.is_file():
                findings.require(event.get("evidence") == sha256_file(evidence_path), f"workflow event {index}: completion evidence digest is stale")
            globally_active = None
        states[feature] = new_state
    findings.require(parsed_times == sorted(parsed_times), "workflow event log is not chronological")
    for feature_id, entry in feature_by_id.items():
        event_state = states.get(str(feature_id))
        expected_state = {"done": "completed", "in_progress": "active"}.get(entry.get("state"))
        if expected_state is not None:
            findings.require(event_state == expected_state, f"{feature_id}: manifest state differs from final workflow event")
        else:
            findings.require(event_state is None, f"{feature_id}: unstarted manifest feature has workflow events")
    return workflow


# Complexity: time O(n), Omega(n), tight Theta(n) in changelog bytes n;
# auxiliary space O(n) for loaded text.
def validate_changelog(findings: Findings) -> None:
    text = (ROOT / "docs/CHANGELOG.md").read_text(encoding="utf-8")
    findings.require(text.startswith("# Changelog\n\n## Unreleased\n"), "changelog lacks leading Unreleased section")
    findings.require("pending local change" not in text, "changelog uses noncanonical pending commit marker")
    marker = "current commit; hash assigned by Git after commit"
    findings.require(text.count(marker) == 1, "changelog must contain exactly one canonical current-commit marker")


# Complexity: time O(r log r + d), Omega(r + d), where r is requirements and d
# blocker text; auxiliary space O(r + d) for the rendered document.
def render_requirements(registry: dict[str, Any]) -> str:
    lines = [
        "# Bifrost requirement trace\n",
        "Generated from `governance/requirements.toml`; do not edit by hand.\n",
        "| Requirement | Owner | Status | Blockers | Admission |",
        "| --- | --- | --- | --- | --- |",
    ]
    for requirement_id, record in sorted(registry["requirements"].items()):
        blockers = ", ".join(f"`{item}`" for item in record["blocking_dependencies"]) or "none"
        lines.append(f"| {requirement_id} | `{record['owner']}` | {record['status']} | {blockers} | {record['admission']} |")
    lines.append("")
    return "\n".join(lines)


# Complexity: time O(d + g), Omega(d), tight Theta(d + g) for dependencies d
# and gate strings g; auxiliary space O(d + g) for the rendered document.
def render_phase0(phase0: dict[str, Any]) -> str:
    lines = [
        "# Bifrost Phase 0 dashboard\n",
        "Generated from `governance/phase0.toml`; do not edit by hand.\n",
        f"Gate status: **{phase0['status']}**",
        f"Beta/stable runtime allowed: **{str(phase0['beta_stable_runtime_allowed']).lower()}**\n",
        f"Out-of-alpha implementation allowed: **{str(phase0['out_of_alpha_implementation_allowed']).lower()}**\n",
        f"Minimum dependency grade: **{phase0['minimum_dependency_grade']}**\n",
        "| Dependency | Revision | Grade | Grade evidence | Evidence revision | Grade reviewer | Grade review | Gates | Review | Admission | Gaps |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in phase0["dependencies"]:
        gates = f"{len(entry['passed_gates'])}/{len(entry['required_gates'])}"
        gaps = "<br>".join(entry["gaps"]) or "none"
        evidence_revision = entry["grade_evidence_revision"] or "unbound"
        reviewer = entry["grade_reviewer"] or "unassigned"
        lines.append(f"| `{entry['id']}` | `{entry['revision']}` | {entry['grade']} | {len(entry['grade_evidence'])} | `{evidence_revision}` | `{reviewer}` | {entry['grade_review']} | {gates} | {entry['review']} | {entry['admission']} | {gaps} |")
    lines.append("")
    return "\n".join(lines)


# Complexity: time O(d + g), Omega(d), tight Theta(d + g) for dependencies d
# and gate strings g; auxiliary space O(d + g) for the rendered document.
def render_alpha(alpha: dict[str, Any]) -> str:
    lines = [
        "# Bifrost learning-alpha dashboard\n",
        "Generated from `governance/alpha.toml`; do not edit by hand.\n",
        f"Gate status: **{alpha['status']}**",
        f"Source implementation Phase-0 exempt: **{str(alpha['source_implementation_phase0_exempt']).lower()}**",
        f"Offline simulation Phase-0 exempt: **{str(alpha['offline_simulation_phase0_exempt']).lower()}**",
        f"Workflow activation required: **{str(alpha['workflow_activation_required']).lower()}**",
        f"Host-network mutation allowed: **{str(alpha['host_network_mutation_allowed']).lower()}**",
        f"Installer-disk mutation allowed: **{str(alpha['installer_disk_mutation_allowed']).lower()}**",
        f"Alpha distribution allowed: **{str(alpha['alpha_distribution_allowed']).lower()}**",
        f"Production allowed: **{str(alpha['production_allowed']).lower()}**\n",
        f"Safety gates: **{len(alpha['passed_safety_gates'])}/{len(alpha['required_safety_gates'])}**\n",
        "| Dependency | Required version | Selected version | Revision | Gates | Review | Admission | Gaps |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in alpha["dependencies"]:
        gates = f"{len(entry['passed_gates'])}/{len(entry['required_gates'])}"
        gaps = "<br>".join(entry["gaps"]) or "none"
        selected = entry["selected_version"] or "unselected"
        revision = entry["revision"] or "unpinned"
        lines.append(f"| `{entry['id']}` | `{entry['required_version']}` | `{selected}` | `{revision}` | {gates} | {entry['review']} | {entry['admission']} | {gaps} |")
    lines.append("")
    return "\n".join(lines)


# Complexity: time O(f + e), Omega(f), tight Theta(f + e) for features f and
# dependency/blocker/evidence strings e; auxiliary space O(f + e).
def render_workflow(workflow: dict[str, Any]) -> str:
    lines = [
        "# Bifrost workflow status\n",
        "Generated from `workflow.toml`; do not edit by hand.\n",
        f"Profile: **{workflow['profile']}**",
        f"Active feature: **`{workflow['active']}`**",
        f"Runtime code allowed in meta repo: **{str(workflow['policy']['runtime_code_allowed']).lower()}**",
        f"External actions allowed: **{str(workflow['policy']['external_actions_allowed']).lower()}**\n",
        "| Feature | State | Phase | Risk | Dependencies | Plan | Review | Evidence | Blockers |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in workflow["features"]:
        dependencies = "<br>".join(f"`{item}`" for item in entry["dependencies"]) or "none"
        blockers = "<br>".join(entry["blockers"]) or "none"
        plan = f"`{entry['plan']}`" if entry.get("plan") else "complete"
        lines.append(f"| `{entry['id']}` | {entry['state']} | {entry['phase']} | {entry['risk']} | {dependencies} | {plan} | {entry['review']} | {len(entry['evidence'])} | {blockers} |")
    lines.append("")
    return "\n".join(lines)


# Complexity: time O(s + e + g), Omega(s), tight Theta(s + e + g) for
# subsystems s, evidence e, and gaps g; auxiliary space O(s + e + g).
def render_coverage(workflow: dict[str, Any]) -> str:
    lines = [
        "# Bifrost global coverage map\n",
        "Generated from `workflow.toml`; do not edit by hand.\n",
        "This records governance and system-evidence posture. It does not claim runtime coverage where artifacts do not exist.\n",
        "| Subsystem | Owner | Risk | Required harness | Evidence | Known gaps | Plan | Next increment |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in workflow["coverage_subsystems"]:
        harness = "<br>".join(f"`{item}`" for item in entry["required_harness"])
        gaps = "<br>".join(entry["known_gaps"]) or "none"
        plan = f"`{entry['plan']}`" if entry.get("plan") else "complete"
        lines.append(f"| `{entry['id']}` | {entry['owner']} | {entry['risk']} | {harness} | {len(entry['evidence'])} | {gaps} | {plan} | {entry['next_increment']} |")
    lines.append("")
    return "\n".join(lines)


# Complexity: time O(n), Omega(n), tight Theta(n) in rendered bytes n;
# auxiliary space O(n); writes are atomic per file via pathlib replacement is
# not guaranteed, so generation is documentation-only and Git retains rollback.
def render_views(registry: dict[str, Any], phase0: dict[str, Any], alpha: dict[str, Any], workflow: dict[str, Any], check: bool, findings: Findings) -> None:
    views = {
        ROOT / "docs/REQUIREMENTS.md": render_requirements(registry),
        ROOT / "docs/PHASE0.md": render_phase0(phase0),
        ROOT / "docs/ALPHA.md": render_alpha(alpha),
        ROOT / "docs/WORKFLOW.md": render_workflow(workflow),
        ROOT / "workflow/COVERAGE.md": render_coverage(workflow),
    }
    for path, expected in views.items():
        if check:
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            findings.require(actual == expected, f"generated view is stale: {path.relative_to(ROOT)}")
        else:
            temporary = path.with_name(f"{path.name}.tmp")
            temporary.write_text(expected, encoding="utf-8")
            temporary.replace(path)


# Complexity: time O(n), Omega(n), tight Theta(n) over all governed metadata
# and documents n; auxiliary space O(n) for parsed records and findings.
def run_validation(check_generated: bool = True) -> Findings:
    findings = Findings()
    try:
        registry = validate_requirements(findings)
        catalog = validate_components(findings)
        phase0 = validate_phase0(findings, catalog)
        alpha = validate_alpha(findings, catalog)
        validate_release(findings, catalog, phase0, alpha)
        validate_schemas(findings)
        validate_deployment_profiles(findings)
        validate_kubernetes_ha(findings)
        validate_goka(findings)
        validate_ha_profiles(findings)
        validate_adrs_and_templates(findings)
        validate_test_lab(findings)
        validate_repository_boundary(findings)
        validate_ci(findings)
        workflow = validate_workflow(findings)
        validate_changelog(findings)
        if check_generated:
            render_views(registry, phase0, alpha, workflow, True, findings)
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as error:
        findings.add(f"validator could not complete: {error}")
    return findings


# Complexity: time O(n), Omega(n), tight Theta(n) for parsed arguments and
# governed repository bytes; auxiliary space O(n) through delegated validators.
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "render" and not args.check:
        findings = Findings()
        registry = validate_requirements(findings)
        phase0 = load_toml("governance/phase0.toml")
        alpha = load_toml("governance/alpha.toml")
        workflow = load_toml("workflow.toml")
        if findings.errors:
            for error in findings.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        render_views(registry, phase0, alpha, workflow, False, findings)
        print("rendered requirements, Phase 0, alpha, workflow, and coverage views")
        return 0

    findings = run_validation(check_generated=True)
    if findings.errors:
        for error in findings.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Bifrost governance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
