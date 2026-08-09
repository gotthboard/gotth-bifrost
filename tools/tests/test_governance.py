import json
import tomllib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from tools import governance


class GovernanceTests(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        findings = governance.run_validation(check_generated=True)
        self.assertEqual([], findings.errors)

    def test_switching_domain_is_composed_and_strict(self) -> None:
        with (governance.ROOT / "governance/components.toml").open("rb") as handle:
            catalog = tomllib.load(handle)
        with (governance.ROOT / "governance/releases/v0.1.toml").open("rb") as handle:
            release = tomllib.load(handle)
        schema = json.loads((governance.ROOT / "schemas/v1/switch-plan.schema.json").read_text())
        components = {entry["id"]: entry for entry in catalog["components"]}
        self.assertIn("bfw-switching", components)
        self.assertEqual(["bfw-core", "bfw-plugin-sdk", "bfw-network"], components["bfw-switching"]["dependencies"])
        self.assertIn("bfw-switching", release["included"])
        self.assertNotIn("bfw-switching", release["deferred"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual("bfw.switch-plan/v1", schema["properties"]["schema"]["const"])
        self.assertTrue(schema["properties"]["rollback_required"]["const"])

    def test_deployment_roles_are_one_product_with_distinct_effects(self) -> None:
        with (governance.ROOT / "governance/deployment-profiles.toml").open("rb") as handle:
            policy = tomllib.load(handle)
        profiles = {entry["id"]: entry for entry in policy["profiles"]}
        self.assertEqual({"router", "switch", "converged"}, set(profiles))
        self.assertFalse(policy["management_address_is_transit"])
        self.assertEqual({"standalone", "fabric"}, set(policy["product_scopes"]))
        self.assertEqual(["standalone"], policy["v0_1_scopes"])
        self.assertIn("user-layer2-bridge-forwarding", profiles["router"]["denied_effects"])
        self.assertEqual({"wan-edge-routing", "nat", "stateful-transport-policy"}, set(profiles["switch"]["denied_effects"]))
        self.assertEqual({2, 3}, set(profiles["switch"]["data_plane_layers"]))
        self.assertEqual({3, 4}, set(profiles["router"]["data_plane_layers"]))
        self.assertEqual({2, 3, 4}, set(profiles["converged"]["data_plane_layers"]))
        self.assertIn("bfw-routing", profiles["switch"]["required_components"])
        self.assertIn("svi-inter-vlan-routing", profiles["switch"]["enabled_effects"])
        self.assertIn("layer2-switching", profiles["converged"]["enabled_effects"])
        self.assertIn("layer3-routing", profiles["converged"]["enabled_effects"])
        self.assertTrue(all("management-termination" in profile["enabled_effects"] for profile in profiles.values()))
        self.assertTrue(all(profile["transition_policy"] == "commit-confirmed" for profile in profiles.values()))

    def test_native_go_ids_contract_is_deferred_and_bounded(self) -> None:
        with (governance.ROOT / "governance/components.toml").open("rb") as handle:
            catalog = tomllib.load(handle)
        components = {entry["id"]: entry for entry in catalog["components"]}
        ids = components["bfw-ids"]
        self.assertEqual("deferred", ids["status"])
        self.assertIn("Native Go Snort-class", ids["responsibility"])
        self.assertIn("bfw-firewall", ids["dependencies"])
        self.assertIn("agent-keyring", ids["dependencies"])
        self.assertIn("agent-filesystem", ids["dependencies"])
        schema = json.loads((governance.ROOT / "schemas/v1/ids-plan.schema.json").read_text())
        self.assertEqual(["passive-ids", "inline-ips"], schema["properties"]["mode"]["enum"])
        self.assertTrue(schema["properties"]["rollback_required"]["const"])
        self.assertEqual("inline-ips", schema["allOf"][0]["if"]["properties"]["mode"]["const"])
        self.assertEqual("object", schema["allOf"][0]["then"]["properties"]["inline_policy"]["type"])
        self.assertEqual("null", schema["allOf"][0]["else"]["properties"]["inline_policy"]["type"])
        self.assertFalse(schema["additionalProperties"])

    def test_distributed_fabric_is_deferred_and_does_not_own_domains(self) -> None:
        with (governance.ROOT / "governance/components.toml").open("rb") as handle:
            catalog = tomllib.load(handle)
        components = {entry["id"]: entry for entry in catalog["components"]}
        fabric = components["bfw-fabric"]
        self.assertEqual("deferred", fabric["status"])
        self.assertIn("without owning those domains", fabric["responsibility"])
        for dependency in ("bfw-switching", "bfw-routing", "bfw-firewall", "bfw-ha", "bfw-frr"):
            self.assertIn(dependency, fabric["dependencies"])
        self.assertIn("rpc-plugin-system", fabric["dependencies"])
        self.assertIn("agent-keyring", fabric["dependencies"])
        self.assertNotIn("bfw-identity", fabric["dependencies"])
        schema = json.loads((governance.ROOT / "schemas/v1/fabric-plan.schema.json").read_text())
        self.assertEqual(3, schema["properties"]["nodes"]["minItems"])
        self.assertEqual("deny-mutations", schema["properties"]["failure_policy"]["properties"]["minority"]["const"])
        self.assertTrue(schema["properties"]["rollback_required"]["const"])

    def test_representative_schema_instances_fail_closed(self) -> None:
        fixture_dir = governance.ROOT / "schemas/v1/fixtures"
        schema_dir = governance.ROOT / "schemas/v1"
        for path in sorted(fixture_dir.glob("*.json")):
            fixture = json.loads(path.read_text())
            schema = json.loads((schema_dir / fixture["schema_file"]).read_text())
            errors = governance.schema_instance_errors(schema, fixture["instance"], schema_dir)
            self.assertEqual(fixture["valid"], not errors, f"{path.name}: {errors}")

    def test_fabric_all_null_placement_is_rejected(self) -> None:
        schema_dir = governance.ROOT / "schemas/v1"
        schema = json.loads((schema_dir / "fabric-plan.schema.json").read_text())
        fixture = json.loads((schema_dir / "fixtures/fabric-plan.invalid.json").read_text())
        errors = governance.schema_instance_errors(schema, fixture["instance"], schema_dir)
        self.assertTrue(any("anyOf" in error for error in errors))

    def test_kubernetes_ha_is_first_party_and_forwarding_independent(self) -> None:
        with (governance.ROOT / "governance/components.toml").open("rb") as handle:
            catalog = tomllib.load(handle)
        with (governance.ROOT / "governance/kubernetes-ha.toml").open("rb") as handle:
            policy = tomllib.load(handle)
        components = {entry["id"]: entry for entry in catalog["components"]}
        controller = components["bfw-kubernetes-controller"]
        self.assertEqual("planned", controller["status"])
        self.assertNotIn("bfw-ha", controller["dependencies"])
        self.assertNotIn("bfw-fabric", controller["dependencies"])
        self.assertFalse(policy["worker_membership_required"])
        self.assertEqual("autonomous-last-known-good", policy["forwarding_dependency"])
        self.assertEqual("freeze-mutations-retain-forwarding", policy["control_loss_policy"])
        profiles = {entry["id"]: entry for entry in policy["profiles"]}
        self.assertFalse(profiles["single-controller"]["ha"])
        self.assertEqual("management-single-point-of-failure", profiles["single-controller"]["availability_claim"])
        self.assertTrue(profiles["ha-controller"]["ha"])
        self.assertGreaterEqual(profiles["ha-controller"]["minimum_controllers"], 3)
        self.assertEqual(1, profiles["ha-controller"]["minimum_controllers"] % 2)

    def test_kubernetes_ha_schema_rejects_one_node_as_ha(self) -> None:
        schema_dir = governance.ROOT / "schemas/v1"
        schema = json.loads((schema_dir / "kubernetes-ha-profile.schema.json").read_text())
        fixture = json.loads((schema_dir / "fixtures/kubernetes-ha-profile.invalid.json").read_text())
        errors = governance.schema_instance_errors(schema, fixture["instance"], schema_dir)
        self.assertTrue(errors)

    def test_goka_is_clean_room_and_has_no_direct_effect_authority(self) -> None:
        with (governance.ROOT / "governance/goka.toml").open("rb") as handle:
            policy = tomllib.load(handle)
        with (governance.ROOT / "governance/components.toml").open("rb") as handle:
            catalog = tomllib.load(handle)
        components = {entry["id"]: entry for entry in catalog["components"]}
        self.assertEqual("GoKA", components["bfw-ha"]["product_name"])
        self.assertTrue(policy["clean_room"])
        self.assertEqual("Go", policy["implementation_language"])
        for field in ("keepalived_source_allowed", "keepalived_library_allowed", "keepalived_binary_allowed", "keepalived_runtime_allowed", "keepalived_configuration_authority", "arbitrary_shell_health_allowed"):
            self.assertFalse(policy[field])
        self.assertEqual("exact-versioned-subset-hard-reject", policy["keepalived_import"])

    def test_goka_schema_rejects_invalid_protocol_and_peer_combination(self) -> None:
        schema_dir = governance.ROOT / "schemas/v1"
        schema = json.loads((schema_dir / "goka-plan.schema.json").read_text())
        fixture = json.loads((schema_dir / "fixtures/goka-plan.invalid.json").read_text())
        errors = governance.schema_instance_errors(schema, fixture["instance"], schema_dir)
        self.assertTrue(errors)
        self.assertEqual(255, schema["properties"]["priority"]["maximum"])

    def test_exact_two_first_party_ha_profiles(self) -> None:
        with (governance.ROOT / "governance/ha-profiles.toml").open("rb") as handle:
            policy = tomllib.load(handle)
        self.assertEqual({"goka-native", "kubernetes-managed"}, set(policy["profiles"]))
        self.assertFalse(policy["simultaneous_management_coordinators_allowed"])
        self.assertEqual("bfw-core", policy["canonical_authority"])
        self.assertEqual("native-node", policy["fast_failover_authority"])
        contracts = {entry["id"]: entry for entry in policy["profile_contracts"]}
        self.assertEqual("goka", contracts["goka-native"]["management_coordinator"])
        self.assertFalse(contracts["goka-native"]["external_controller_substrate_required"])
        self.assertEqual("kubernetes", contracts["kubernetes-managed"]["management_coordinator"])
        self.assertTrue(contracts["kubernetes-managed"]["external_controller_substrate_required"])
        self.assertTrue(all(entry["first_party"] and entry["packaged_out_of_box"] for entry in contracts.values()))

    def test_ha_profile_schema_rejects_mismatched_coordinator(self) -> None:
        schema_dir = governance.ROOT / "schemas/v1"
        schema = json.loads((schema_dir / "ha-deployment-profile.schema.json").read_text())
        fixture = json.loads((schema_dir / "fixtures/ha-deployment-profile.invalid.json").read_text())
        self.assertTrue(governance.schema_instance_errors(schema, fixture["instance"], schema_dir))

    def test_dependency_cycle_is_reported(self) -> None:
        graph = {"bfw-a": ["bfw-b"], "bfw-b": ["bfw-c"], "bfw-c": ["bfw-a"]}
        self.assertEqual(
            ["bfw-a", "bfw-b", "bfw-c", "bfw-a"],
            governance.find_dependency_cycle(graph),
        )

    def test_acyclic_dependencies_pass(self) -> None:
        graph = {"bfw-a": ["bfw-b"], "bfw-b": [], "bfw-c": ["bfw-a"]}
        self.assertEqual([], governance.find_dependency_cycle(graph))

    def test_reference_collection_is_recursive(self) -> None:
        value = {"items": [{"$ref": "one.json"}], "nested": {"$ref": "two.json#/$defs/x"}}
        self.assertEqual(["one.json", "two.json#/$defs/x"], list(governance.collect_refs(value)))

    def test_requirement_evidence_cannot_be_laundered_across_features(self) -> None:
        scopes = {
            "sha256:" + "a" * 64: {"BFW-PRD-079"},
            "sha256:" + "b" * 64: {"BFW-PRD-080"},
        }
        self.assertTrue(governance.has_requirement_bound_evidence("BFW-PRD-079", ["sha256:" + "a" * 64], scopes))
        self.assertFalse(governance.has_requirement_bound_evidence("BFW-PRD-079", ["sha256:" + "b" * 64], scopes))

    def test_requirement_render_is_stable(self) -> None:
        registry = {
            "requirements": {
                "BFW-PRD-001": {
                    "owner": "bfw-core",
                    "status": "defined",
                    "blocking_dependencies": ["BFW-PHASE-0"],
                    "admission": "not_admitted",
                }
            }
        }
        rendered = governance.render_requirements(registry)
        self.assertIn("| BFW-PRD-001 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |", rendered)
        self.assertEqual(rendered, governance.render_requirements(registry))

    def test_phase0_render_does_not_hide_blockers(self) -> None:
        phase0 = {
            "status": "blocked",
            "beta_stable_runtime_allowed": False,
            "out_of_alpha_implementation_allowed": False,
            "minimum_dependency_grade": "A",
            "dependencies": [{
                "id": "agent-keyring",
                "revision": "0" * 40,
                "grade": "ungraded",
                "grade_evidence": [],
                "grade_review": "not_started",
                "passed_gates": [],
                "required_gates": ["windows", "review"],
                "review": "not_started",
                "admission": "not_admitted",
                "gaps": ["native evidence absent"],
            }],
        }
        rendered = governance.render_phase0(phase0)
        self.assertIn("Beta/stable runtime allowed: **false**", rendered)
        self.assertIn("Out-of-alpha implementation allowed: **false**", rendered)
        self.assertIn("Minimum dependency grade: **A**", rendered)
        self.assertIn("0/2", rendered)
        self.assertIn("native evidence absent", rendered)

    def test_alpha_render_does_not_hide_effect_boundaries(self) -> None:
        alpha = {
            "status": "blocked",
            "source_implementation_phase0_exempt": True,
            "offline_simulation_phase0_exempt": True,
            "workflow_activation_required": True,
            "host_network_mutation_allowed": False,
            "installer_disk_mutation_allowed": False,
            "alpha_distribution_allowed": False,
            "production_allowed": False,
            "required_safety_gates": ["disk", "packet-policy"],
            "passed_safety_gates": [],
            "dependencies": [{
                "id": "rpc-plugin-system",
                "required_version": "2.x",
                "selected_version": "",
                "revision": "",
                "passed_gates": [],
                "required_gates": ["identity", "liveness"],
                "review": "not_started",
                "admission": "not_admitted",
                "gaps": ["v2 release absent"],
            }],
        }
        rendered = governance.render_alpha(alpha)
        self.assertIn("Source implementation Phase-0 exempt: **true**", rendered)
        self.assertIn("Workflow activation required: **true**", rendered)
        self.assertIn("Host-network mutation allowed: **false**", rendered)
        self.assertIn("Production allowed: **false**", rendered)
        self.assertIn("v2 release absent", rendered)

    def test_stale_generated_view_fails_closed(self) -> None:
        registry = {
            "requirements": {
                "BFW-PRD-000": {
                    "owner": "meta",
                    "status": "defined",
                    "blocking_dependencies": [],
                    "admission": "not_admitted",
                }
            }
        }
        phase0 = {
            "status": "blocked",
            "beta_stable_runtime_allowed": False,
            "out_of_alpha_implementation_allowed": False,
            "minimum_dependency_grade": "A",
            "dependencies": [],
        }
        alpha = {
            "status": "blocked",
            "source_implementation_phase0_exempt": True,
            "offline_simulation_phase0_exempt": True,
            "workflow_activation_required": True,
            "host_network_mutation_allowed": False,
            "installer_disk_mutation_allowed": False,
            "alpha_distribution_allowed": False,
            "production_allowed": False,
            "required_safety_gates": [],
            "passed_safety_gates": [],
            "dependencies": [],
        }
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/REQUIREMENTS.md").write_text("stale\n")
            (root / "docs/PHASE0.md").write_text("stale\n")
            (root / "docs/ALPHA.md").write_text("stale\n")
            findings = governance.Findings()
            with mock.patch.object(governance, "ROOT", root):
                governance.render_views(registry, phase0, alpha, True, findings)
            self.assertEqual(3, len(findings.errors))
            self.assertTrue(all("generated view is stale" in error for error in findings.errors))

    def test_incomplete_admitted_component_fails_closed(self) -> None:
        catalog = {
            "components": [{
                "id": "bfw-core",
                "kind": "core",
                "responsibility": "test",
                "repository": "",
                "revision": "",
                "artifact_digests": [],
                "api_version": "0.1-draft",
                "schema_version": "1-draft",
                "ui_version": "none",
                "dependencies": [],
                "conflicts": [],
                "platforms": [],
                "platform_status": "unassessed",
                "migration_order": 0,
                "rollback_mate": "",
                "evidence_hashes": [],
                "status": "planned",
                "admission": "admitted",
            }],
            "external_dependencies": [],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=catalog):
            governance.validate_components(findings)
        joined = "\n".join(findings.errors)
        for field in ("repository", "immutable revision", "artifact digest", "platform declaration", "rollback mate", "evidence"):
            self.assertIn(field, joined)

    def test_phase0_beta_stable_permission_cannot_outrun_admission(self) -> None:
        catalog = {
            "external_dependencies": [{
                "id": "agent-keyring",
                "revision": "0" * 40,
                "admission": "not_admitted",
            }]
        }
        phase0 = {
            "status": "passed",
            "beta_stable_runtime_allowed": True,
            "out_of_alpha_implementation_allowed": True,
            "applies_to_channels": ["beta", "stable"],
            "alpha_gate": "BFW-ALPHA-0",
            "minimum_dependency_grade": "A",
            "dependencies": [{
                "id": "agent-keyring",
                "revision": "0" * 40,
                "required_gates": ["review"],
                "passed_gates": [],
                "evidence": [],
                "gaps": ["missing"],
                "review": "not_started",
                "admission": "not_admitted",
                "grade": "ungraded",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=phase0):
            governance.validate_phase0(findings, catalog)
        joined = "\n".join(findings.errors)
        self.assertIn("beta/stable runtime flag", joined)
        self.assertIn("out-of-alpha implementation flag", joined)
        self.assertIn("status", joined)

    def test_phase0_admission_rejects_below_a_dependency(self) -> None:
        revision = "0" * 40
        catalog = {
            "external_dependencies": [{
                "id": "agent-keyring",
                "revision": revision,
                "admission": "not_admitted",
            }]
        }
        phase0 = {
            "status": "blocked",
            "beta_stable_runtime_allowed": False,
            "out_of_alpha_implementation_allowed": False,
            "applies_to_channels": ["beta", "stable"],
            "alpha_gate": "BFW-ALPHA-0",
            "minimum_dependency_grade": "A",
            "dependencies": [{
                "id": "agent-keyring",
                "revision": revision,
                "required_gates": ["review"],
                "passed_gates": ["review"],
                "evidence": ["sha256:" + "a" * 64],
                "gaps": [],
                "review": "passed",
                "admission": "admitted",
                "grade": "B+",
                "grade_evidence": ["sha256:" + "b" * 64],
                "grade_evidence_revision": revision,
                "grade_reviewer": "independent-bifrost-review",
                "grade_review": "passed",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=phase0):
            governance.validate_phase0(findings, catalog)
        joined = "\n".join(findings.errors)
        self.assertIn("invalid Phase 0 grade", joined)
        self.assertIn("below A grade", joined)

    def test_phase0_a_grade_requires_revision_bound_independent_evidence(self) -> None:
        revision = "0" * 40
        catalog = {
            "external_dependencies": [{
                "id": "agent-keyring",
                "revision": revision,
                "admission": "not_admitted",
            }]
        }
        phase0 = {
            "status": "passed",
            "beta_stable_runtime_allowed": True,
            "out_of_alpha_implementation_allowed": True,
            "applies_to_channels": ["beta", "stable"],
            "alpha_gate": "BFW-ALPHA-0",
            "minimum_dependency_grade": "A",
            "dependencies": [{
                "id": "agent-keyring",
                "revision": revision,
                "required_gates": ["review"],
                "passed_gates": ["review"],
                "evidence": ["sha256:" + "a" * 64],
                "gaps": [],
                "review": "passed",
                "admission": "admitted",
                "grade": "A",
                "grade_evidence": [],
                "grade_evidence_revision": "",
                "grade_reviewer": "",
                "grade_review": "not_started",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=phase0):
            governance.validate_phase0(findings, catalog)
        joined = "\n".join(findings.errors)
        self.assertIn("grade lacks evidence", joined)
        self.assertIn("not bound to the admitted revision", joined)
        self.assertIn("lacks an independent reviewer", joined)
        self.assertIn("grade review has not passed", joined)
        self.assertIn("out-of-alpha implementation flag", joined)

    def test_alpha_mutation_permission_cannot_outrun_minimum_gate(self) -> None:
        catalog = {
            "external_dependencies": [{
                "id": "rpc-plugin-system",
                "revision": "0" * 40,
                "admission": "not_admitted",
            }]
        }
        alpha = {
            "gate_id": "BFW-ALPHA-0",
            "full_admission_gate": "BFW-PHASE-0",
            "status": "passed",
            "source_implementation_phase0_exempt": True,
            "offline_simulation_phase0_exempt": True,
            "workflow_activation_required": True,
            "host_network_mutation_allowed": True,
            "installer_disk_mutation_allowed": True,
            "alpha_distribution_allowed": True,
            "production_allowed": False,
            "platform": "linux",
            "distribution": "alpine",
            "architecture": "x86_64",
            "runtime_contract": "rpc-plugin-system-v2",
            "required_safety_gates": ["disk"],
            "passed_safety_gates": [],
            "evidence": [],
            "review": "not_started",
            "admission": "not_admitted",
            "dependencies": [{
                "id": "rpc-plugin-system",
                "required_version": "2.x",
                "selected_version": "",
                "revision": "",
                "required_gates": ["identity"],
                "passed_gates": [],
                "evidence": [],
                "gaps": ["missing"],
                "review": "not_started",
                "admission": "not_admitted",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=alpha):
            governance.validate_alpha(findings, catalog)
        joined = "\n".join(findings.errors)
        self.assertIn("host_network_mutation_allowed", joined)
        self.assertIn("installer_disk_mutation_allowed", joined)
        self.assertIn("alpha_distribution_allowed", joined)
        self.assertIn("status", joined)

    def test_alpha_rejects_rpc_plugin_v1_selection(self) -> None:
        revision = "0" * 40
        catalog = {
            "external_dependencies": [{
                "id": "rpc-plugin-system",
                "revision": revision,
                "admission": "not_admitted",
            }]
        }
        alpha = {
            "gate_id": "BFW-ALPHA-0",
            "full_admission_gate": "BFW-PHASE-0",
            "status": "blocked",
            "source_implementation_phase0_exempt": True,
            "offline_simulation_phase0_exempt": True,
            "workflow_activation_required": True,
            "host_network_mutation_allowed": False,
            "installer_disk_mutation_allowed": False,
            "alpha_distribution_allowed": False,
            "production_allowed": False,
            "platform": "linux",
            "distribution": "alpine",
            "architecture": "x86_64",
            "runtime_contract": "rpc-plugin-system-v2",
            "required_safety_gates": ["disk"],
            "passed_safety_gates": [],
            "evidence": [],
            "review": "not_started",
            "admission": "not_admitted",
            "dependencies": [{
                "id": "rpc-plugin-system",
                "required_version": "2.x",
                "selected_version": "1.9.9",
                "revision": revision,
                "status": "blocked",
                "required_gates": ["identity"],
                "passed_gates": [],
                "evidence": [],
                "gaps": ["wrong major"],
                "review": "not_started",
                "admission": "not_admitted",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=alpha):
            governance.validate_alpha(findings, catalog)
        self.assertIn("selected version is not v2", "\n".join(findings.errors))


if __name__ == "__main__":
    unittest.main()
