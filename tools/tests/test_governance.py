import copy
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

    def test_alpine_live_media_produces_machine_tailored_install(self) -> None:
        workflow = governance.load_toml("workflow.toml")
        feature = next(
            entry
            for entry in workflow["features"]
            if entry["id"] == "alpine-linux-appliance-iso-v1"
        )
        self.assertEqual("planned", feature["state"])
        self.assertEqual(
            [f"BFW-PRD-{number}" for number in range(209, 215)],
            feature["requirements"],
        )
        self.assertEqual(["routing-switching-protocol-suites-v1"], feature["dependencies"])
        self.assertTrue(any("hardware matrix" in item for item in feature["blockers"]))
        self.assertTrue(any("tailoring" in item for item in feature["acceptance"]))
        self.assertTrue(any("machine-tailored" in item for item in feature["acceptance"]))
        self.assertTrue(any("recovery" in item for item in feature["acceptance"]))

        catalog = governance.load_toml("governance/components.toml")
        installer = next(
            entry for entry in catalog["components"] if entry["id"] == "bfw-installer"
        )
        self.assertIn("deterministic machine tailoring", installer["responsibility"])
        self.assertEqual("distribution-component", installer["kind"])
        self.assertEqual([], installer["dependencies"])
        self.assertEqual([], installer["platforms"])
        self.assertEqual("planned", installer["status"])

        release = governance.load_toml("governance/releases/v0.1.toml")
        self.assertIn("bfw-updater", release["included"])
        self.assertEqual(["bfw-installer"], release["build_components"])
        self.assertNotIn("bfw-installer", release["included"])
        self.assertNotIn("bfw-installer", release["deferred"])
        self.assertEqual(
            {"bfw-installer"},
            {entry["id"] for entry in release["build_composition"]},
        )

        alpha = governance.load_toml("governance/alpha.toml")
        self.assertIn("deterministic-machine-tailoring", alpha["required_safety_gates"])
        self.assertIn("apk-ownership-integrity", alpha["required_safety_gates"])

        lab = governance.load_toml("governance/test-lab.toml")
        target = next(entry for entry in lab["targets"] if entry["id"] == "linux-primary")
        self.assertEqual(["amd64"], target["architectures"])
        self.assertEqual("unpinned", target["status"])
        self.assertIn("generic Alpine Linux live ISO", target["role"])
        self.assertIn("machine-tailored", target["role"])

        required_tests = set(lab["required_scenarios"])
        self.assertIn("alpine-machine-inventory-build-plan", required_tests)
        self.assertIn("alpine-machine-apk-kernel-initramfs-closure", required_tests)
        self.assertIn("alpine-generic-recovery-boot-apk-ownership", required_tests)

        plan = (
            governance.ROOT
            / "workflow/features/alpine-linux-appliance-iso-v1/DECOMPOSITION.md"
        ).read_text()
        self.assertIn("machine-tailored", plan)
        self.assertIn("APK ownership", plan)
        self.assertIn("signed generic recovery", plan)

        prd = " ".join((governance.ROOT / "documents/PRD.md").read_text().split())
        implementation = " ".join(
            (governance.ROOT / "documents/IMPLEMENTATION-SPEC.md")
            .read_text()
            .split()
        )
        release_plan = " ".join(
            (governance.ROOT / "workflow/RELEASE-COMPOSITION-PLAN.md")
            .read_text()
            .split()
        )
        self.assertIn("installed system shall be tailored to the detected machine", prd)
        self.assertIn("rebuilding all of Alpine on the target is unsupported", prd)
        self.assertIn("signed generic recovery kernel/initramfs/environment", prd)
        self.assertIn("shall not delete or modify APK-owned files", implementation)
        self.assertIn("ISO contains no release-signing private key", implementation)
        self.assertIn("normalized hardware inventory, machine plan", release_plan)
        self.assertNotIn("installed-image digest", release_plan)

    def test_freebsd_live_media_produces_machine_tailored_install(self) -> None:
        workflow = governance.load_toml("workflow.toml")
        feature = next(
            entry
            for entry in workflow["features"]
            if entry["id"] == "freebsd-generic-appliance-iso-v1"
        )
        self.assertEqual("planned", feature["state"])
        self.assertEqual(
            [f"BFW-PRD-{number}" for number in range(223, 229)],
            feature["requirements"],
        )
        self.assertEqual(
            ["routing-switching-protocol-suites-v1", "alpine-linux-appliance-iso-v1"],
            feature["dependencies"],
        )
        self.assertTrue(any("hardware matrix" in item for item in feature["blockers"]))
        self.assertTrue(any("tailoring" in item for item in feature["acceptance"]))
        self.assertTrue(any("machine-tailored" in item for item in feature["acceptance"]))
        self.assertTrue(any("recovery" in item for item in feature["acceptance"]))

        catalog = governance.load_toml("governance/components.toml")
        installer = next(
            entry for entry in catalog["components"] if entry["id"] == "bfw-installer"
        )
        self.assertEqual("distribution-component", installer["kind"])
        self.assertEqual([], installer["platforms"])
        self.assertEqual([], installer["dependencies"])

        lab = governance.load_toml("governance/test-lab.toml")
        target = next(
            entry for entry in lab["targets"] if entry["id"] == "freebsd-generic-x86-64"
        )
        self.assertEqual(["amd64"], target["architectures"])
        self.assertEqual("unpinned", target["status"])
        self.assertIn("generic x86-64", target["role"])
        self.assertIn("machine-tailored", target["role"])

        required_tests = set(lab["required_scenarios"])
        self.assertIn("freebsd-machine-inventory-build-plan", required_tests)
        self.assertIn(
            "freebsd-machine-kernel-module-firmware-package-closure",
            required_tests,
        )
        self.assertIn("freebsd-generic-recovery-boot", required_tests)

        plan = (
            governance.ROOT
            / "workflow/features/freebsd-generic-appliance-iso-v1/DECOMPOSITION.md"
        ).read_text()
        self.assertIn("universal x86-64 hardware support", plan)
        self.assertIn("machine-tailored system", plan)
        self.assertIn("Separately distributed prebuilt hardware-specific", plan)
        self.assertIn("never admission evidence", plan)

        prd = " ".join((governance.ROOT / "documents/PRD.md").read_text().split())
        implementation = " ".join(
            (governance.ROOT / "documents/IMPLEMENTATION-SPEC.md")
            .read_text()
            .split()
        )
        self.assertIn("machine-tailored installed system", prd)
        self.assertIn("full on-target source build is an explicit optional slow path", prd)
        self.assertIn("signed generic recovery kernel/environment", prd)
        self.assertNotIn("Hardware-specific appliance images are deferred", prd)
        self.assertIn("ISO shall contain no release-signing private key", implementation)
        self.assertIn("Separately distributed prebuilt hardware-specific media", implementation)

    def test_release_schema_admits_alpha_and_binds_platform_evidence(self) -> None:
        schema = governance.load_json(governance.ROOT / "schemas/v1/release.schema.json")
        self.assertEqual(
            {"development", "alpha", "beta", "stable"},
            set(schema["properties"]["channel"]["enum"]),
        )
        self.assertIn("builders", schema["required"])
        platform_required = set(
            schema["properties"]["platforms"]["items"]["required"]
        )
        self.assertEqual(
            {"name", "image_digest", "hardware_matrix_digest", "evidence_hashes"},
            platform_required,
        )
        self.assertEqual(
            "#/$defs/artifactRecord",
            schema["properties"]["builders"]["items"]["$ref"],
        )

    def test_component_admission_requires_assessed_platform_and_dependencies(self) -> None:
        revision = "0" * 40
        digest = "sha256:" + "a" * 64
        catalog = {
            "platforms": {"known": ["linux"], "admitted": ["linux"]},
            "components": [
                {
                    "id": "bfw-dependency",
                    "kind": "test",
                    "responsibility": "test dependency",
                    "repository": "https://example.invalid/dependency.git",
                    "revision": revision,
                    "artifact_digests": [digest],
                    "api_version": "1.0",
                    "schema_version": "1.0",
                    "ui_version": "none",
                    "dependencies": [],
                    "conflicts": [],
                    "platforms": ["linux"],
                    "platform_status": "assessed",
                    "migration_order": 1,
                    "rollback_mate": revision,
                    "evidence_hashes": [digest],
                    "status": "planned",
                    "admission": "not_admitted",
                },
                {
                    "id": "bfw-consumer",
                    "kind": "test",
                    "responsibility": "test consumer",
                    "repository": "https://example.invalid/consumer.git",
                    "revision": revision,
                    "artifact_digests": [digest],
                    "api_version": "1.0",
                    "schema_version": "1.0",
                    "ui_version": "none",
                    "dependencies": ["bfw-dependency"],
                    "conflicts": [],
                    "platforms": ["linux"],
                    "platform_status": "unassessed",
                    "migration_order": 2,
                    "rollback_mate": revision,
                    "evidence_hashes": [digest],
                    "status": "planned",
                    "admission": "admitted",
                },
            ],
            "external_dependencies": [],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=catalog):
            governance.validate_components(findings)
        joined = "\n".join(findings.errors)
        self.assertIn("admitted component platform state is not assessed", joined)
        self.assertIn("admitted component has non-admitted dependencies", joined)

        catalog["components"][1]["admission"] = "not_admitted"
        catalog["components"][1]["platform_status"] = "unsupported"
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=catalog):
            governance.validate_components(findings)
        self.assertNotIn("invalid platform status", "\n".join(findings.errors))

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
                "grade_evidence_revision": "",
                "grade_reviewer": "",
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
        self.assertIn("`unbound`", rendered)
        self.assertIn("`unassigned`", rendered)
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
                "admission": "admitted",
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
        workflow = {
            "profile": "strict",
            "active": "example-v1",
            "policy": {
                "runtime_code_allowed": False,
                "external_actions_allowed": False,
            },
            "features": [{
                "id": "example-v1",
                "state": "in_progress",
                "phase": "design",
                "risk": "high",
                "dependencies": [],
                "review": "pending",
                "evidence": [],
                "blockers": ["independent review"],
            }],
            "coverage_subsystems": [{
                "id": "example",
                "owner": "meta",
                "risk": "high",
                "required_harness": ["unit"],
                "evidence": [],
                "known_gaps": ["evidence absent"],
                "next_increment": "Run the harness.",
            }],
        }
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "workflow").mkdir()
            (root / "docs/REQUIREMENTS.md").write_text("stale\n")
            (root / "docs/PHASE0.md").write_text("stale\n")
            (root / "docs/ALPHA.md").write_text("stale\n")
            (root / "docs/WORKFLOW.md").write_text("stale\n")
            (root / "workflow/COVERAGE.md").write_text("stale\n")
            findings = governance.Findings()
            with mock.patch.object(governance, "ROOT", root):
                governance.render_views(registry, phase0, alpha, workflow, True, findings)
            self.assertEqual(5, len(findings.errors))
            self.assertTrue(all("generated view is stale" in error for error in findings.errors))

    def workflow_findings(self, mutate) -> list[str]:
        workflow = copy.deepcopy(governance.load_toml("workflow.toml"))
        mutate(workflow)
        original_load = governance.load_toml

        def load(path: str):
            return workflow if path == "workflow.toml" else original_load(path)

        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", side_effect=load):
            governance.validate_workflow(findings)
        return findings.errors

    def test_workflow_rejects_duplicate_feature_ids(self) -> None:
        errors = self.workflow_findings(
            lambda workflow: workflow["features"].append(copy.deepcopy(workflow["features"][0]))
        )
        self.assertTrue(any("duplicate feature IDs" in error for error in errors))

    def test_workflow_rejects_multiple_active_features(self) -> None:
        def mutate(workflow) -> None:
            workflow["features"][-1]["state"] = "in_progress"

        errors = self.workflow_findings(mutate)
        self.assertTrue(any("exactly one registered active feature" in error for error in errors))

    def test_workflow_rejects_dependency_cycles(self) -> None:
        def mutate(workflow) -> None:
            workflow["features"][0]["dependencies"] = [workflow["active"]]

        errors = self.workflow_findings(mutate)
        self.assertTrue(any("workflow dependency cycle" in error for error in errors))

    def test_workflow_done_requires_bound_evidence(self) -> None:
        def mutate(workflow) -> None:
            workflow["features"][0]["evidence"] = []

        errors = self.workflow_findings(mutate)
        self.assertTrue(any("done workflow lacks evidence" in error for error in errors))

    def test_unfinished_workflow_requires_checked_plan(self) -> None:
        def mutate(workflow) -> None:
            active = next(entry for entry in workflow["features"] if entry["id"] == workflow["active"])
            active.pop("plan")

        errors = self.workflow_findings(mutate)
        self.assertTrue(any("unfinished workflow lacks a checked plan" in error for error in errors))

    def test_unresolved_high_risk_coverage_requires_checked_plan(self) -> None:
        def mutate(workflow) -> None:
            unresolved = next(entry for entry in workflow["coverage_subsystems"] if not entry["evidence"])
            unresolved.pop("plan")

        errors = self.workflow_findings(mutate)
        self.assertTrue(any("unresolved high-risk coverage lacks a checked plan" in error for error in errors))

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
                "admission": "admitted",
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
                "admission": "admitted",
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
                "admission": "admitted",
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
                "admission": "admitted",
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

    def test_phase0_accepts_complete_revision_bound_a_grade(self) -> None:
        revision = "0" * 40
        catalog = {
            "external_dependencies": [{
                "id": "agent-keyring",
                "revision": revision,
                "admission": "admitted",
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
                "status": "passed",
                "required_gates": ["review"],
                "passed_gates": ["review"],
                "evidence": ["sha256:" + "a" * 64],
                "gaps": [],
                "review": "passed",
                "admission": "admitted",
                "grade": "A",
                "grade_evidence": ["sha256:" + "b" * 64],
                "grade_evidence_revision": revision,
                "grade_reviewer": "independent-bifrost-review",
                "grade_review": "passed",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=phase0):
            governance.validate_phase0(findings, catalog)
        self.assertEqual([], findings.errors)

    def test_phase0_cannot_outrun_component_catalog_admission(self) -> None:
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
                "status": "passed",
                "required_gates": ["review"],
                "passed_gates": ["review"],
                "evidence": ["sha256:" + "a" * 64],
                "gaps": [],
                "review": "passed",
                "admission": "admitted",
                "grade": "A",
                "grade_evidence": ["sha256:" + "b" * 64],
                "grade_evidence_revision": revision,
                "grade_reviewer": "independent-bifrost-review",
                "grade_review": "passed",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=phase0):
            governance.validate_phase0(findings, catalog)
        errors = "\n".join(findings.errors)
        self.assertIn("admission outruns component catalog admission", errors)
        self.assertIn("status does not match complete dependency admission state", errors)
        self.assertIn("beta/stable runtime flag does not match complete admission state", errors)
        self.assertIn("out-of-alpha implementation flag does not match complete A-grade admission state", errors)
        self.assertIn("Phase 0 status does not match complete admission state", errors)

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

    def test_alpha_accepts_complete_minimum_admission(self) -> None:
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
            "passed_safety_gates": ["disk"],
            "evidence": ["sha256:" + "a" * 64],
            "review": "passed",
            "admission": "alpha_admitted",
            "dependencies": [{
                "id": "rpc-plugin-system",
                "required_version": "2.x",
                "selected_version": "2.0.0",
                "revision": revision,
                "status": "passed",
                "required_gates": ["identity"],
                "passed_gates": ["identity"],
                "evidence": ["sha256:" + "b" * 64],
                "gaps": [],
                "review": "passed",
                "admission": "alpha_admitted",
            }],
        }
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=alpha):
            governance.validate_alpha(findings, catalog)
        self.assertEqual([], findings.errors)

    def test_release_admission_cannot_outrun_channel_gate(self) -> None:
        catalog = {"components": []}
        blocked_phase0 = {"beta_stable_runtime_allowed": False}
        blocked_alpha = {"alpha_distribution_allowed": False}
        base_release = {
            "status": "passed",
            "admission": "admitted",
            "alpha_gate": "BFW-ALPHA-0",
            "phase0_gate": "BFW-PHASE-0",
            "phase0_required_for": ["beta", "stable"],
            "release_manifest_schema": "bfw.release/v1",
            "included": [],
            "build_components": [],
            "deferred": [],
            "composition": [],
            "build_composition": [],
        }
        cases = {
            "alpha": "alpha admission outruns BFW-ALPHA-0 distribution permission",
            "beta": "beta/stable admission outruns complete BFW-PHASE-0 admission",
            "stable": "beta/stable admission outruns complete BFW-PHASE-0 admission",
        }
        for channel, expected in cases.items():
            with self.subTest(channel=channel):
                release = {**base_release, "channel": channel}
                findings = governance.Findings()
                with mock.patch.object(governance, "load_toml", return_value=release):
                    governance.validate_release(findings, catalog, blocked_phase0, blocked_alpha)
                self.assertIn(expected, "\n".join(findings.errors))

        admitted_phase0 = {"beta_stable_runtime_allowed": True}
        admitted_alpha = {"alpha_distribution_allowed": True}
        for channel in cases:
            with self.subTest(channel=channel, gates="admitted"):
                release = {**base_release, "channel": channel}
                findings = governance.Findings()
                with mock.patch.object(governance, "load_toml", return_value=release):
                    governance.validate_release(findings, catalog, admitted_phase0, admitted_alpha)
                self.assertEqual([], findings.errors)

        inconsistent = {**base_release, "channel": "alpha", "status": "blocked"}
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=inconsistent):
            governance.validate_release(findings, catalog, admitted_phase0, admitted_alpha)
        self.assertIn("release status does not match admission state", "\n".join(findings.errors))

        design_release = {**base_release, "channel": "design"}
        findings = governance.Findings()
        with mock.patch.object(governance, "load_toml", return_value=design_release):
            governance.validate_release(findings, catalog, admitted_phase0, admitted_alpha)
        self.assertIn("design profile cannot become an admitted release", "\n".join(findings.errors))


if __name__ == "__main__":
    unittest.main()
