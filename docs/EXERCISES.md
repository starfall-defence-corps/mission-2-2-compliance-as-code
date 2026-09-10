# Mission 2.2: Compliance as Code — Exercises

**Rank**: Lieutenant
**Prerequisite**: Module 1 complete + [Mission 2.1 (Weapon Handling Test)](https://github.com/starfall-defence-corps/mission-2-1-weapon-handling-test)

---

## Phase 0: Activate Your Environment

```bash
make setup
source venv/bin/activate
```

Verify 4 containers are running: `docker ps` should show cis-target, sdc-web, sdc-db, sdc-comms.

---

## Phase 1: Understanding CIS Benchmarks

Before the obstacle course, you need to understand the framework.

### What CIS Benchmarks Are

CIS Benchmarks are industry-consensus security configuration standards maintained by the **Center for Internet Security**. They define measurable, repeatable security controls for operating systems, cloud platforms, applications, and network devices.

Each control has:
- A **control ID** (e.g., 5.2.7)
- A **description** (e.g., "Ensure SSH MaxAuthTries is set to 4 or less")
- A **rationale** (why this matters)
- An **audit** procedure (how to check)
- A **remediation** procedure (how to fix)
- A **level** (Level 1 = basic, Level 2 = strict)

### CIS Controls Relevant to This Mission

| Control | Section | Description | Level |
|---------|---------|-------------|-------|
| 1.5.1 | Initial Setup | Restrict core dumps | L1 |
| 1.7.1 | Initial Setup | Warning banner configured | L1 |
| 3.3.2 | Network | ICMP redirects not accepted | L1 |
| 5.1.8 | Access | Cron restricted to authorised users | L1 |
| 5.2.4 | Access | SSH root login disabled | L1 |
| 5.2.5 | Access | SSH password auth disabled | L1 |
| 5.2.7 | Access | SSH MaxAuthTries 4 or less | L1 |
| 5.2.13 | Access | SSH idle timeout configured | L1 |
| 5.2.16 | Access | SSH LoginGraceTime 60s or less | L1 |
| 6.1.3 | Maintenance | /etc/shadow permissions restricted | L1 |

**CIS control notes**:
- **Core dumps** (CIS 1.5.1): Restricted via `/etc/security/limits.d/` drop-in files. A file containing `* hard core 0` prevents all users from creating core dumps.
- **Login banner** (CIS 1.7.1): `/etc/issue.net` is the SSH pre-login banner (shown before authentication). This is distinct from `/etc/motd` (shown after login).
- **Cron access** (CIS 5.1.8): When `/etc/cron.allow` exists, only users listed in it may use cron. Creating the file with just `root` restricts cron to root only.

### Mapping Controls to Ansible Tasks

Every CIS control maps to one or more Ansible tasks. The key insight: **CIS tells you WHAT, Ansible tells the system HOW.**

```yaml
# CIS 5.2.7 — Ensure SSH MaxAuthTries is set to 4 or less
- name: "CIS 5.2.7 — Set SSH MaxAuthTries"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?MaxAuthTries'
    line: "MaxAuthTries 4"
  notify: restart ssh
  tags: [cis_5_2]
```

**Tags** are critical. They let you run specific controls:
```bash
ansible-playbook site.yml --tags cis_5_2    # Only SSH controls
ansible-playbook site.yml --tags cis_6_1    # Only file permissions
ansible-playbook site.yml                    # All controls
```

### What Ansible Tags Are

Tags are labels you attach to tasks. When you run `ansible-playbook --tags cis_5_2`, only tasks tagged with `cis_5_2` execute. When you run without `--tags`, all tasks run. Tags enable selective enforcement — apply only SSH controls, only file permissions, or everything at once.

You can assign multiple tags to a task: `tags: [cis_5_2, ssh]`. Use `--skip-tags` to exclude specific tags.

### The sysctl Module

In [Mission 1.3](https://github.com/starfall-defence-corps/mission-1-3-clean-sweep), you hardened kernel parameters by copying a file to `/etc/sysctl.d/`. The `ansible.posix.sysctl` module is the dedicated way to manage individual kernel parameters:

```yaml
- name: "CIS 3.3.2 — Disable ICMP redirects"
  ansible.posix.sysctl:
    name: net.ipv4.conf.all.accept_redirects
    value: "0"
    sysctl_set: true
    reload: true
  tags: [cis_3_3]
```

This module writes the parameter and applies it immediately (`sysctl_set: true`). The `ansible.posix` collection is installed during `make setup`.

### What Lynis Is

**Lynis** is a security auditing tool for Unix systems. It performs hundreds of individual tests and produces a **hardening index** (0-100). Higher is better.

```bash
# Run on a remote host via Ansible
ansible cis-target -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

Output includes:
```
  Hardening index : 52 [##########          ]
  Tests performed : 178
  Plugins enabled : 0
```

**In production**, organisations use tools like **OpenSCAP** (NIST/DISA), **InSpec** (Chef), or commercial scanners (Tenable, Qualys) for automated CIS/STIG compliance scanning. Lynis serves the same educational purpose in our Docker lab.

---

## Phase 2: Obstacle Course — Compliance Range

> **START YOUR TIMER**

### Mission 1: Write the Role (15–20 min)

**Location**: `workspace/obstacle-course/mission-1/`

```bash
cd workspace/obstacle-course/mission-1
```

1. **Read the 8 tests** at `tests/test_cis_hardening.py`. Each test maps to a CIS control.

2. **Create the role**:
   ```bash
   ansible-galaxy init roles/cis_hardening
   ```

3. **Write tasks** in `roles/cis_hardening/tasks/main.yml`:
   - Each task must implement a CIS control
   - Each task must have a `tags` field with the CIS section (e.g., `tags: [cis_5_2]`)
   - You need at least 5 tasks (some tests check multiple things in one task)

4. **Apply the role**:
   ```bash
   ansible-playbook -i inventory.yml site.yml
   ```

5. **Run the tests**:
   ```bash
   pytest tests/ --hosts=ssh://cadet@localhost:2251 \
     --ssh-identity-file=../../.ssh/cadet_key \
     --ssh-config=../../.ssh/testinfra_ssh_config \
     --sudo -v
   ```

6. **Iterate** until all 8 pass.

### Mission 2: Write the Tests (15–20 min)

**Location**: `workspace/obstacle-course/mission-2/`

```bash
cd workspace/obstacle-course/mission-2
```

1. **Read the role**: Examine `roles/compliance_baseline/tasks/main.yml` and `roles/compliance_baseline/defaults/main.yml`. The role claims to implement CIS controls, but it has **bugs**.

   > **Note**: The buggy role uses `{{ sysctl_settings | dict2items }}` to loop over a dictionary. The `dict2items` filter converts `{key1: val1, key2: val2}` into `[{key: key1, value: val1}, ...]` for use in loops.

2. **Apply the role**:
   ```bash
   ansible-playbook -i inventory.yml site.yml
   ```

3. **Write tests** at `tests/test_compliance_baseline.py`. Include:
   - Basic checks: SSH service running, banner deployed, cron.allow exists
   - CIS compliance checks: verify actual values match CIS requirements
   - Find the bugs — at least 3 controls are misconfigured or missing

4. **Run your tests**:
   ```bash
   pytest tests/test_compliance_baseline.py --hosts=ssh://cadet@localhost:2251 \
     --ssh-identity-file=../../.ssh/cadet_key \
     --ssh-config=../../.ssh/testinfra_ssh_config \
     --sudo -v
   ```

5. **Expected result**: Basic tests pass. Compliance tests for buggy controls **fail**. That's correct — failing tests prove the bugs exist.

> **STOP YOUR TIMER**

| Time | Rating |
|------|--------|
| Under 35 min | Gold Standard |
| 35–45 min | Compliant |
| 45–55 min | Improving |
| 55–70 min | Needs Work |
| 70+ min | Audit Failed — retry |

---

## Phase 3: Main Mission — The Baseline Sprint (H-45)

**Location**: `workspace/main-mission/`

```bash
cd workspace/main-mission
```

> **START YOUR SPRINT TIMER.** Readiness exercise VOIDBREAKER goes hot in 45 minutes.
> Baseline all three fleet nodes to CIS Level 1 before the window opens.

Build a complete CIS Level 1 compliance solution for the fleet — but this time the clock is part of the test. You will not finish all controls on all nodes by working top-to-bottom. **Triage.**

### Triage — Work the Fleet Wide Before Deep

Apply controls in priority order (from [BRIEFING §3f](BRIEFING.md)), and apply each tier to **all three nodes** before moving to the next. If the clock beats you, P1-everywhere beats P3-on-one-node.

| Priority | Controls | Run with |
|----------|----------|----------|
| **P1 — Credential defence** | 5.2.4 root login off · 5.2.5 password auth off · 5.2.7 MaxAuthTries ≤4 | `ansible-playbook site.yml --tags cis_5_2` |
| **P2 — Surface & persistence** | 5.2.13 idle timeout · 5.2.16 LoginGraceTime ≤60s · 5.1.8 cron restricted · 3.3.2 ICMP redirects off | `--tags cis_5_1,cis_3_3,cis_5_2` (the SSH timeouts share `cis_5_2` with P1 — re-running it is free, skipping it leaves them unset) |
| **P3 — Evidence & hygiene** | 6.1.3 shadow perms · 1.5.1 core dumps · 1.7.1 banner | `--tags cis_6_1,cis_1_5,cis_1_7` |

Your tags are what make triage *executable*: `--tags cis_5_2` lets you push credential defence to the whole fleet in one command, then move on. That is why every task must be tagged.

> **Timing ladder** (honour-system — ARIA grades correctness, the clock is for you):
>
> | Time to baseline all 3 nodes | Rating |
> |------------------------------|--------|
> | Under 30 min | Ahead of the window — full readiness |
> | 30–45 min | Baselined before H-hour — mission success |
> | 45–60 min | Window opened mid-sprint — partial exposure |
> | 60+ min | Fleet met the adversary unhardened — after-action review |

### Step 1: Bring Your Role

Copy your `fleet_hardening` role from [Mission 1.5](https://github.com/starfall-defence-corps/mission-1-5-clean-house) (or recreate it):

```bash
mkdir -p roles
cp -r /path/to/mission-1-5/workspace/roles/fleet_hardening roles/
```

### Step 2: Create Inventory

Create `inventory/hosts.yml` and `inventory/group_vars/` for the fleet.

| Node | OS | Port |
|------|----|------|
| sdc-web | Ubuntu 22.04 | 2221 |
| sdc-db | Rocky Linux 9 | 2222 |
| sdc-comms | Ubuntu 22.04 | 2223 |

### Step 3: Create ansible.cfg and site.yml

Same patterns as previous missions.

### Step 4: Baseline Lynis Scan

Before hardening, measure the current state:

```bash
ansible all -i inventory/hosts.yml -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

Record the hardening index for each node in `COMPLIANCE.md`.

### Step 5: Extend Role with CIS Controls

Add CIS Level 1 tasks to your role. At minimum:

- SSH: MaxAuthTries, LoginGraceTime, ClientAliveInterval (CIS 5.2.x)
- Files: /etc/shadow permissions (CIS 6.1.x)
- Kernel: sysctl hardening — disable redirects (CIS 3.x)
- Access: cron.allow, core dump limits (CIS 1.5.x, 5.1.x)
- Banner: /etc/issue.net with warning message (CIS 1.7.x)

**Tag every task** with its CIS section.

### Step 6: Deploy and Rescan

```bash
ansible-playbook -i inventory/hosts.yml site.yml

# Rescan
ansible all -i inventory/hosts.yml -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

Record the new hardening index. You should see a significant improvement.

### Step 7: Write Tests

Create `tests/test_fleet_compliance.py` with **at least 10 test functions**:

- SSH root login disabled
- SSH password auth disabled
- SSH MaxAuthTries set to 4
- SSH idle timeout configured
- Firewall active (both OS families)
- MOTD or banner deployed
- /etc/shadow permissions correct
- Core dumps restricted
- Sysctl hardened (IP forwarding, redirects)
- Telnet removed from Debian nodes

### Step 8: Create Molecule Configuration

```bash
mkdir -p molecule/default
```

Write `molecule/default/molecule.yml` using the pattern from Mission 2.1.

### Step 9: Run Tests and Complete Report

```bash
# Run tests against all fleet nodes
pytest tests/ \
  --hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223 \
  --ssh-identity-file=../.ssh/cadet_key \
  --ssh-config=../.ssh/testinfra_ssh_config \
  --sudo -v
```

Complete `COMPLIANCE.md` with all Lynis scores and control statuses.

### Step 10: Verify with ARIA

```bash
cd ../..   # Back to mission root
make test
```

All 3 phases must pass.

---

## Further Reading

- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — Free PDF downloads (registration required)
- [Lynis Documentation](https://cisofy.com/lynis/)
- [OpenSCAP](https://www.open-scap.org/) — Enterprise-grade SCAP scanner used in production
- [DISA STIGs](https://public.cyber.mil/stigs/) — DoD security baselines

---

Stuck? Consult [HINTS.md](HINTS.md) for troubleshooting.

---

*SDC Cyber Command — 2187 — LIEUTENANT EYES ONLY*
