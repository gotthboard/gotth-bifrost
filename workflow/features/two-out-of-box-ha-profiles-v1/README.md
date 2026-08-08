# Two first-party out-of-the-box HA profiles

Status: completed

Bifrost supports exactly `goka-native` and `kubernetes-managed` as first-party
HA deployment profiles. Both ship as Bifrost composition choices once HA is
release-admitted and use the same canonical core contracts.

Only one management coordinator owns an HA domain. Kubernetes management does
not replace node-local fast failover, and v0.1 remains honestly unadmitted.
