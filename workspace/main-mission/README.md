# Main Mission: Compliance as Code

Extend your `fleet_hardening` role with CIS Level 1 controls. Deploy to the fleet. Measure compliance with Lynis.

## What You Build

1. **Inventory** at `inventory/hosts.yml` with `group_vars/` for the 3-node fleet
2. **CIS-hardened role** at `roles/fleet_hardening/` (copy from 1.5, then extend)
3. **Ansible configuration** at `ansible.cfg`
4. **Playbook** at `site.yml` calling your role
5. **Molecule scenario** at `molecule/default/molecule.yml`
6. **Tests** at `tests/test_fleet_compliance.py` with at least 10 test functions
7. **Compliance report** at `COMPLIANCE.md`

## CIS Controls to Implement

At minimum, your role must implement these CIS Level 1 controls:

| Control | Description | Tag |
|---------|-------------|-----|
| CIS 1.5.1 | Restrict core dumps | `cis_1_5` |
| CIS 1.7.1 | Warning banner configured | `cis_1_7` |
| CIS 3.3.2 | ICMP redirects not accepted | `cis_3_3` |
| CIS 5.1.8 | Cron restricted to authorised users | `cis_5_1` |
| CIS 5.2.4 | SSH root login disabled | `cis_5_2` |
| CIS 5.2.5 | SSH password auth disabled | `cis_5_2` |
| CIS 5.2.7 | SSH MaxAuthTries 4 or less | `cis_5_2` |
| CIS 5.2.13 | SSH idle timeout configured | `cis_5_2` |
| CIS 6.1.3 | /etc/shadow permissions | `cis_6_1` |

Plus any additional hardening from your Module 1 role (telnet removed, firewall active, MOTD, etc).

## Lynis Scanning

Run Lynis before and after applying your role:

```bash
# Before (on one node)
ansible sdc-web -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"

# After applying role
ansible sdc-web -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

Record the hardening index in `COMPLIANCE.md`.

## Fleet Topology

| Node | OS | Port |
|------|----|------|
| sdc-web | Ubuntu 22.04 | 2221 |
| sdc-db | Rocky Linux 9 | 2222 |
| sdc-comms | Ubuntu 22.04 | 2223 |
