# Optional Kubernetes-managed HA

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature defines dedicated Kubernetes/K3s controller deployment as an
optional Bifrost management HA profile. It supports one honestly non-HA
controller or an odd quorum of at least three failure-separated controllers.

Managed routers and switches remain native autonomous Bifrost nodes. Loss of
the controller, API, etcd, CNI, storage, or management path freezes new
mutations but cannot interrupt last-known-good forwarding, fast network HA, or
local recovery.
