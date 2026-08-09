# GoKA clean-room native Go HA

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature formalizes GoKA as the clean-room native Go HA engine behind
`bfw-ha`. Public VRRP specifications and independently authored tests are its
implementation authority; Keepalived is neither source nor runtime authority.

GoKA owns election, typed health, and failover intent. Bifrost's core, network,
routing, firewall, and platform owners authorize and apply all native effects.
