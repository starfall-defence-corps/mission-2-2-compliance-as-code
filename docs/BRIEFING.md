---
CLASSIFICATION: LIEUTENANT EYES ONLY
MISSION: 2.2 — COMPLIANCE AS CODE
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# MISSION 2.2 — COMPLIANCE AS CODE

> **FLASH TRAFFIC — H-45.** SDC Cyber Command has scheduled readiness exercise
> **VOIDBREAKER**. At H-hour the range goes hot: the adversary-emulation cell begins
> live probing of the fleet. You have **45 minutes** to baseline every node to a CIS
> Level 1 standard before the window opens. You cannot implement 200+ controls in 45
> minutes. **Triage. Harden the controls that stop the most likely attacks — first.**

---

## 1. SITUATION

### 1a. Enemy Forces

**Corsair Unpatched** has been running the fleet's compliance program. His method: a spreadsheet. Last updated: 2019. "If it works, don't update it." His nodes pass no benchmark. His audit evidence is a screenshot of a terminal from three years ago — and now the exercise clock is running against every corner he cut.

Default SSH settings, unrestricted core dumps, wide-open cron access on every node — the adversary-emulation cell doesn't need zero-days to walk through doors Corsair left open. When VOIDBREAKER goes hot, whatever you haven't baselined is fair game.

### 1b. Friendly Forces

You know how to harden systems (Module 1). You know how to test them ([Mission 2.1](https://github.com/starfall-defence-corps/mission-2-1-weapon-handling-test)). Now you learn two things at once: to measure compliance against an industry standard — the **CIS Benchmarks** — and to **triage under a clock**. When the window is 45 minutes and the control set is 200-plus, the operator who knows *which controls matter most* baselines the whole fleet; the one who works top-to-bottom hardens one node and meets the adversary on the other two.

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

Implement CIS Level 1 controls as Ansible tasks. Measure compliance. Prove improvement — and in the main mission, get the fleet baselined **before the exercise window opens**.

| Phase | Description | Framing |
|-------|-------------|---------|
| Obstacle Course Mission 1 | Given CIS tests, write the role | Pre-flight rehearsal — build muscle memory |
| Obstacle Course Mission 2 | Given buggy role, write tests that catch gaps | Pre-flight rehearsal — learn to spot gaps |
| Main Mission — **Baseline Sprint** | CIS-harden the fleet against the clock, measure with Lynis | H-45: the real thing, triaged and timed |

The obstacle course is your rehearsal: no live adversary, drill the mechanics until the CIS-control-to-Ansible-task translation is automatic. The main mission is the sprint: same skills, but now the clock and the triage decision are the test.

---

## 3. EXECUTION

### 3a. Commander's Intent

Compliance is not a checkbox — it's code, and under an exercise clock it's a *triage* decision. Every control maps to an Ansible task. Every task has a CIS tag. Every deployment is measurable. But when the window is 45 minutes wide, "harden everything" is not a plan — **harden the highest-impact controls across the whole fleet first, then deepen.** Corsair Unpatched's spreadsheet dies today; the habit of hardening wide before deep is what you carry into [Noise Storm (2.5)](https://github.com/starfall-defence-corps/mission-2-5-noise-storm), when the probing is no longer emulated.

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

### 3f. Triage Priority — What to Baseline First

You have ten controls and forty-five minutes across three nodes. Work them in **priority order**, applying each priority tier to the *whole fleet* before you move to the next. If the clock beats you, you want P1 done everywhere — not P3 done on one node.

| Priority | Controls | Why these first |
|----------|----------|-----------------|
| **P1 — Credential defence** | 5.2.4 root login off · 5.2.5 password auth off · 5.2.7 MaxAuthTries ≤4 | Credential attacks — brute force, password spray, root SSH — are the adversary's opening move. This is exactly what hits you in Noise Storm (2.5). Shutting the front door buys the most survival per minute. |
| **P2 — Surface & persistence** | 5.2.13 idle timeout · 5.2.16 LoginGraceTime ≤60s · 5.1.8 cron restricted · 3.3.2 ICMP redirects off | Shrinks the ways an intruder moves laterally and keeps a foothold. High value once the door is shut. |
| **P3 — Evidence & hygiene** | 6.1.3 shadow perms · 1.5.1 core dumps · 1.7.1 login banner | Defence-in-depth and audit hygiene. The banner is legal/cosmetic — real, but it stops zero attacks, so it is **last**. |

> **The triage lesson**: you should be able to *justify* this order. A control that blocks the most likely attack outranks a control that is merely required for the checklist. "Wide before deep" — every node gets P1 before any node gets P3.

---

## 4. OBSTACLE COURSE TIMING (PRE-FLIGHT REHEARSAL)

> **START YOUR TIMER** at the beginning of the Obstacle Course. This is a skills drill — build speed before the sprint.

| Time | Rating |
|------|--------|
| Under 35 min | Gold Standard |
| 35–45 min | Compliant |
| 45–55 min | Improving |
| 55–70 min | Needs Work |
| 70+ min | Audit Failed — retry |

> **STOP YOUR TIMER** after both obstacle course missions pass.

---

## 5. THE BASELINE SPRINT (MAIN MISSION) — H-45

> **START YOUR SPRINT TIMER** when you begin the main mission (from your first Lynis baseline scan). **STOP** when `make test` confirms all three fleet nodes are baselined and tested.

Work the triage tiers in order (§3f), fleet-wide. Your rating is how much of the fleet you baselined before exercise VOIDBREAKER went hot:

| Time to baseline all 3 nodes | Rating |
|------------------------------|--------|
| Under 30 min | **Ahead of the window** — full readiness, P1–P3 fleet-wide with margin |
| 30–45 min | **Baselined before H-hour** — mission success |
| 45–60 min | **Window opened mid-sprint** — partial exposure; note which nodes were still soft |
| 60+ min | **Fleet met the adversary unhardened** — after-action review: what would you triage differently? |

> This timer is honour-system, like the obstacle course — ARIA grades correctness, not the clock. The clock is for *you*: it forces the triage decision that makes the skill real.

---

## 6. COMMAND AND SIGNAL

**Commander's Final Order**: Corsair Unpatched's reign of "it works, don't touch it" ends here. Compliance is code. Measurable. Repeatable. Auditable. Every CIS control is an Ansible task. Every task has a tag. Every deployment improves the hardening index — and when the exercise clock is running, you baseline wide before you baseline deep.

When ARIA confirms all three phases, Corsair Unpatched is relieved of duty and the fleet meets VOIDBREAKER hardened.

**Start your timer. Begin.**

---

## 7. GETTING STARTED

1. Activate your environment: `source venv/bin/activate`
2. Follow the step-by-step guide: [EXERCISES.md](EXERCISES.md)
3. Stuck? Consult [HINTS.md](HINTS.md)
4. Track your progress: [CHECKLIST.md](../CHECKLIST.md)

---

*SDC Cyber Command — 2187 — LIEUTENANT EYES ONLY*
