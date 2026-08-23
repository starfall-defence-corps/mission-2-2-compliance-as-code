---
CLASSIFICATION: LIEUTENANT JG EYES ONLY
MISSION: 2.2 — COMPLIANCE AS CODE
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# MISSION 2.2 — COMPLIANCE AS CODE

---

## 1. SITUATION

### 1a. Enemy Forces

**Corsair Unpatched** has been running the fleet's compliance program. His method: a spreadsheet. Last updated: 2019. "If it works, don't update it." His nodes pass no benchmark. His audit evidence is a screenshot of a terminal from three years ago.

The Voidborn don't need zero-days when Corsair Unpatched leaves default SSH settings, unrestricted core dumps, and wide-open cron access on every node.

### 1b. Friendly Forces

You know how to harden systems (Module 1). You know how to test them (Mission 2.1). Now you learn to measure compliance against an industry standard — the **CIS Benchmarks** — and prove your hardening is correct, repeatable, and auditable.

### 1c. What CIS Benchmarks Are

The **Center for Internet Security (CIS) Benchmarks** are industry-consensus security baselines. Over 200 controls per OS, organised into sections:

| Section | Category |
|---------|----------|
| 1 | Initial Setup (filesystems, core dumps, banners) |
| 2 | Services (inetd, mail, NFS) |
| 3 | Network Configuration (sysctl, firewall) |
| 4 | Logging and Auditing |
| 5 | Access, Authentication, Authorization (SSH, PAM, cron) |
| 6 | System Maintenance (file permissions, user accounts) |

**Level 1**: Basic hardening. Minimal performance impact. What every server should have.
**Level 2**: Stricter. May limit functionality. For high-security environments.

In military contexts, **STIGs** (Security Technical Implementation Guides) serve the same purpose but are DoD-specific and stricter. Same concept, different authority.

### 1d. Attachments / Support

**ARIA** will verify your work across three phases. Run `make test` at any time.

**Lynis** is pre-installed on all containers. Use it to measure your hardening index before and after applying your role.

---

## 2. MISSION

Implement CIS Level 1 controls as Ansible tasks. Measure compliance. Prove improvement.

| Phase | Description |
|-------|-------------|
| Obstacle Course Mission 1 | Given CIS tests, write the role |
| Obstacle Course Mission 2 | Given buggy role, write tests that catch gaps |
| Main Mission | CIS-harden the fleet, measure with Lynis |

---

## 3. EXECUTION

### 3a. Commander's Intent

Compliance is not a checkbox — it's code. Every control maps to an Ansible task. Every task has a CIS tag. Every deployment is measurable. Corsair Unpatched's spreadsheet dies today.

### 3b. Lab Assets

**Compliance Range** (Obstacle Course):

| Designation | OS | SSH Port | Network |
|-------------|----|----------|---------|
| `cis-target` | Ubuntu 22.04 | 2251 | 172.33.0.11 |

**Fleet** (Main Mission):

| Designation | OS | SSH Port | Network |
|-------------|----|----------|---------|
| `sdc-web` | Ubuntu 22.04 | 2221 | 172.33.0.21 |
| `sdc-db` | Rocky Linux 9 | 2222 | 172.33.0.22 |
| `sdc-comms` | Ubuntu 22.04 | 2223 | 172.33.0.23 |

**SSH user**: `cadet` (key-based auth, key at `.ssh/cadet_key`)

### 3c. Known CIS Violations

All containers ship with these violations:

**SSH (CIS 5.2.x)**:
- MaxAuthTries set to 6 (should be 4 or less)
- LoginGraceTime set to 120 (should be 60 or less)
- ClientAliveInterval set to 0 (should be 300)
- Root login enabled, password auth enabled

**Filesystem (CIS 6.1.x)**:
- `/etc/shadow` permissions 0644 (should be 0640)
- `/etc/gshadow` permissions 0644 (should be 0640)

**Kernel (CIS 3.x)**:
- IP forwarding enabled
- ICMP redirects accepted

**Access Control (CIS 5.1.x)**:
- No `/etc/cron.allow` (cron unrestricted)
- No `/etc/at.allow` (at unrestricted)

**Initial Setup (CIS 1.x)**:
- Core dumps unrestricted
- No login banner (`/etc/issue.net` missing)

### 3d. Lynis Quick Reference

```bash
# Full audit (quick mode, no colors for parsing)
lynis audit system --quick --no-colors

# Last 5 lines include the hardening index
lynis audit system --quick --no-colors 2>/dev/null | tail -5

# Via Ansible ad-hoc
ansible sdc-web -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

### 3e. Rules of Engagement

- Every CIS task must have a tag matching the control section (e.g., `tags: [cis_5_2]`)
- Lynis scores are your evidence — record before and after
- You may consult CIS benchmark documentation and Ansible docs
- No looking at other missions' solution files

---

## 4. OBSTACLE COURSE TIMING

> **START YOUR TIMER** at the beginning of the Obstacle Course.

| Time | Rating |
|------|--------|
| Under 35 min | Gold Standard |
| 35–45 min | Compliant |
| 45–55 min | Improving |
| 55–70 min | Needs Work |
| 70+ min | Audit Failed — retry |

> **STOP YOUR TIMER** after both obstacle course missions pass.

---

## 5. COMMAND AND SIGNAL

**Commander's Final Order**: Corsair Unpatched's reign of "it works, don't touch it" ends here. Compliance is code. Measurable. Repeatable. Auditable. Every CIS control is an Ansible task. Every task has a tag. Every deployment improves the hardening index.

When ARIA confirms all three phases, Corsair Unpatched is relieved of duty.

**Start your timer. Begin.**

---

## 6. GETTING STARTED

1. Activate your environment: `source venv/bin/activate`
2. Follow the step-by-step guide: [EXERCISES.md](EXERCISES.md)
3. Stuck? Consult [HINTS.md](HINTS.md)
4. Track your progress: [CHECKLIST.md](../CHECKLIST.md)

---

*SDC Cyber Command — 2187 — LIEUTENANT JG EYES ONLY*
