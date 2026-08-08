# Governance tooling

`governance.py` is a dependency-free structural validator and deterministic
renderer for this meta repository. It intentionally does not:

- validate Bifrost runtime behavior or platform semantics
- verify signatures or contact repositories
- prove JSON instances against every JSON Schema keyword
- execute component test/evidence commands
- decide that missing evidence is admission

Those limits are deliberate. CI metadata success is not product admission.
