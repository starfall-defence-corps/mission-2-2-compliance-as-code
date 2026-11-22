# Starfall Defence Corps Academy

> 🧭 [← 2.1 Weapon Handling Test](https://github.com/starfall-defence-corps/mission-2-1-weapon-handling-test) · **You are here: 2.2 Compliance as Code** · [2.3 Fleet Sync →](https://github.com/starfall-defence-corps/mission-2-3-fleet-sync) · [🏠 Academy Hub](https://github.com/starfall-defence-corps/sdc-academy) · [📚 Field Manuals](https://github.com/starfall-defence-corps/sdc-academy/tree/main/field-manuals)

> ☁️ **No Docker on your machine?** Create your own copy first (Use this template), then on **your** repo: **Code → Codespaces → Create codespace** — everything is preinstalled. First boot takes ~5 min (one-time); after that it starts fast.

## Mission 2.2: Compliance as Code

> *"Readiness exercise VOIDBREAKER goes hot in 45 minutes. Corsair Unpatched hasn't baselined a server since 2019 — 'if it works, don't touch it.' You don't get to harden all 200 controls before the window opens. Triage. Baseline the fleet. Now."*

You are a Lieutenant at the Starfall Defence Corps Academy. You can harden systems. You can test them. Now prove you can measure compliance against an industry standard — **CIS Benchmarks** — implement it as code, and **triage which controls matter most when the clock is running**. The obstacle course is your rehearsal; the main mission is a timed baseline sprint against the exercise window.

## Briefing

**Corsair Unpatched** ran the fleet's compliance programme from a spreadsheet last updated in 2019. Every node ships with his gaps: default SSH settings, loose `/etc/shadow` permissions, accepted ICMP redirects, unrestricted cron and core dumps, no login banner. SDC Cyber Command has scheduled readiness exercise **VOIDBREAKER**, and you have 45 minutes to baseline the fleet to CIS Level 1 before the range goes hot.

You cannot implement every control in that window. The briefing gives you a priority order — **P1** credential defence, **P2** surface and persistence, **P3** evidence and hygiene — and the rule that goes with it: apply each tier to the whole fleet before you start the next. Full orders, the known violations and the triage table are in the [Mission Briefing](docs/BRIEFING.md).

## Objectives

`make test` verifies three phases:

| Phase | Part | ARIA checks |
|-------|------|-------------|
| 1 | Obstacle Course — Mission 1: *Write the Role* | A `cis_hardening` role exists in `workspace/obstacle-course/mission-1/roles/` with at least 5 tasks, at least 3 of them tagged; it applies to `cis-target` without errors; and all 8 provided CIS tests in `tests/test_cis_hardening.py` pass |
| 2 | Obstacle Course — Mission 2: *Write the Tests* | You have written `workspace/obstacle-course/mission-2/tests/test_compliance_baseline.py` with at least 5 test functions; the provided `compliance_baseline` role applies to `cis-target`; and your tests produce a mix of passes (basic checks) and failures (the compliance gaps in the role) |
| 3 | Main Mission: *The Baseline Sprint (H-45)* | `workspace/main-mission/` contains your `fleet_hardening` role with CIS-tagged tasks, a `site.yml`, Testinfra tests with at least 10 test functions, and a filled-in `COMPLIANCE.md` (Lynis scores or control status); and your tests pass against all three fleet nodes after the role is applied |

The main mission's required controls — CIS 1.5.1, 1.7.1, 3.3.2, 5.1.8, 5.2.4, 5.2.5, 5.2.7, 5.2.13, 5.2.16 and 6.1.3, each with its tag — are listed in [`workspace/main-mission/README.md`](workspace/main-mission/README.md).

## What You'll Learn

- What CIS Benchmarks are: sections, Level 1 vs Level 2, and how STIGs relate
- Mapping a CIS control to an Ansible task, and tagging it by section (`tags: [cis_5_2]`)
- Using tags to apply one priority tier fleet-wide (`ansible-playbook … --tags cis_5_2`)
- Triage under a clock: hardening wide before deep
- Kernel hardening with the `ansible.posix.sysctl` module
- Measuring hardening with Lynis before and after, and recording the evidence
- Writing Testinfra tests that expose compliance gaps in an existing role

## Prerequisites

- Completed Module 1 (Missions 1.1–1.6 + Gateway Simulation)
- Completed Mission 2.1 (Weapon Handling Test) — the main mission extends your `fleet_hardening` role and reuses the Molecule + Testinfra skills from 2.1
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- **Ansible**: provided by the lab — `make setup` builds a local venv with `ansible-core`, Molecule and pytest-testinfra; no host install needed
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
# 1. Use this template on GitHub (green button, top right) to create YOUR OWN
#    copy. Set it Public, then clone it:
git clone https://github.com/YOUR-USERNAME/mission-2-2-compliance-as-code.git
cd mission-2-2-compliance-as-code

# 2. Check your machine is mission-ready
make doctor

# 3. Launch the compliance range + fleet (4 containers)
make setup

# 4. Activate the virtual environment
source venv/bin/activate
```

5. **Read your orders**: [Mission Briefing](docs/BRIEFING.md)
6. **Work the phases**: [Exercises](docs/EXERCISES.md)
7. **Stuck?** [Hints & Troubleshooting](docs/HINTS.md)
8. **Track progress**: [Checklist](CHECKLIST.md)
9. **Ready?** `make test`, then `make submit`

Run every command from the **project root** (the folder with the `Makefile`); paths in the docs are relative to it.

## Lab Architecture

```
 Your Machine
+---------------------------------------------------------------+
|  workspace/                                                   |
|    obstacle-course/mission-1/  (given CIS tests → write role)  |
|    obstacle-course/mission-2/  (given role → write tests)      |
|    main-mission/               (role, tests, COMPLIANCE.md)    |
|    .ssh/cadet_key              (auto-generated)                |
|                                                               |
|   Compliance Range             Fleet                          |
|  +------------------+   +----------------------------------+  |
|  | cis-target :2251 |   | sdc-web   :2221  (Ubuntu 22.04)  |  |
|  | Ubuntu 22.04     |   | sdc-db    :2222  (Rocky Linux 9) |  |
|  | CIS violations   |   | sdc-comms :2223  (Ubuntu 22.04)  |  |
|  +------------------+   +----------------------------------+  |
+---------------------------------------------------------------+
```

| Node | Used in | OS | SSH port |
|------|---------|----|----------|
| `cis-target` | Obstacle course (both missions) | Ubuntu 22.04 | 2251 |
| `sdc-web` | Main Mission | Ubuntu 22.04 | 2221 |
| `sdc-db` | Main Mission | Rocky Linux 9 | 2222 |
| `sdc-comms` | Main Mission | Ubuntu 22.04 | 2223 |

Every container ships with the CIS violations listed in the briefing, and Lynis is pre-installed on all of them. All nodes accept SSH as `cadet` with the key `make setup` generates.

## Mission Structure

| Part | Description | Location |
|------|-------------|----------|
| Obstacle Course 1 | *Rehearsal* — given CIS tests, write the role | `workspace/obstacle-course/mission-1/` |
| Obstacle Course 2 | *Rehearsal* — given a buggy role, write tests | `workspace/obstacle-course/mission-2/` |
| Main Mission — **Baseline Sprint** | H-45: triage + CIS-harden the fleet against the clock, measure with Lynis | `workspace/main-mission/` |

Both clocks are honour-system — `make test` grades correctness, not time.

**Obstacle course** (start before Mission 1, stop when both missions pass):

| Time | Rating |
|------|--------|
| Under 35 min | Gold Standard |
| 35–45 min | Compliant |
| 45–55 min | Improving |
| 55–70 min | Needs Work |
| 70+ min | Audit Failed — retry |

**Baseline sprint** (start at your first Lynis baseline scan, stop when `make test` confirms all three fleet nodes):

| Time | Rating |
|------|--------|
| Under 30 min | Ahead of the window |
| 30–45 min | Baselined before H-hour |
| 45–60 min | Window opened mid-sprint |
| 60+ min | Fleet met the adversary unhardened |

## Available Commands

```
make help            Show available commands
make doctor          Check your machine is mission-ready (Docker, ports, tools)
make setup           Launch compliance range + fleet (4 containers)
make test            Ask ARIA to verify your work
make submit          Submit your work for ARIA review (branch, commit, push, PR)
make reset           Destroy and rebuild all nodes
make destroy         Tear down everything
make ssh-cis-target  SSH into cis-target (obstacle course, port 2251)
make ssh-web         SSH into sdc-web (fleet, Ubuntu, port 2221)
make ssh-db          SSH into sdc-db (fleet, Rocky Linux, port 2222)
make ssh-comms       SSH into sdc-comms (fleet, Ubuntu, port 2223)
```

> **Note:** `make submit` uses the [GitHub CLI](https://cli.github.com/) — install `gh` and run `gh auth login` once before your first submission.

## Mission Files

| File | Purpose |
|------|---------|
| [BRIEFING.md](docs/BRIEFING.md) | Mission briefing, known CIS violations and the triage priority table — **read this first** |
| [EXERCISES.md](docs/EXERCISES.md) | Phase-by-phase guide: CIS primer, obstacle course, baseline sprint |
| [HINTS.md](docs/HINTS.md) | Troubleshooting, sprint triage commands, common CIS patterns |
| [CHECKLIST.md](CHECKLIST.md) | Progress tracker |
| [COMPLIANCE.md](workspace/main-mission/COMPLIANCE.md) | Your compliance report: Lynis before/after and control status |

## Checking Your Work: `make test`

`make test` runs ARIA's grader (`molecule/default/tests/test_compliance.py`) against the running lab and reports each objective, phase by phase. For the live checks it applies your playbooks to the containers and runs the Testinfra suites, so the lab must be up (`make setup`). It needs no API key and works offline.

- Run it as often as you like. `make reset` rebuilds the containers if you need a clean start; your `workspace/` files are preserved.
- The mission is complete when all three phases are green.
- Lynis scores are your evidence in `COMPLIANCE.md`; the grader checks that the report is filled in, not that you hit a particular score.

## Submission and ARIA Review

When `make test` is green, `make submit` creates a `mission-submission` branch (or uses your current branch if you are not on `main`), commits `workspace/` and `CHECKLIST.md`, pushes, and opens a pull request to `main` in **your own** copy. You can also do this by hand with `git` and the GitHub web UI.

Opening or updating the pull request runs the **ARIA Review** workflow (`.github/workflows/aria-review.yml`). It does not re-run the grader — the deterministic checks need the Docker lab, so your local `make test` is the verdict. Instead, ARIA reads your submitted workspace files, including `COMPLIANCE.md`, and posts a qualitative, in-character code review as a PR comment. Each new push updates the same comment.

To enable PR reviews, add an API key to your repo:
1. Get a key from [platform.claude.com](https://platform.claude.com/)
2. In your repo: **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
3. Name: `ANTHROPIC_API_KEY`, Value: your key

Without a key, the comment says the review was skipped and the check still passes; `make test` works locally either way.

## Hints Policy

At Lieutenant rank, hints are minimal. [HINTS.md](docs/HINTS.md) covers troubleshooting, the tag commands for running the sprint tier by tier, and a few common CIS task patterns. The provided tests are your specification: read them first, then ARIA's messages in `make test`, then the hints. [EXERCISES.md](docs/EXERCISES.md) is the step-by-step guide if you need it. For deeper reference, see [FM-4 — CIS & Compliance Reference](https://github.com/starfall-defence-corps/sdc-academy/blob/main/field-manuals/FM-4-cis-compliance-reference.md).

## Troubleshooting

**SSH issues**: Run `make setup` first, then check `docker ps` shows all 4 containers. `cis-target` is on port 2251; fleet nodes are on 2221–2223.

**sysctl errors**: Some kernel parameters can't be set inside Docker containers — see [HINTS.md](docs/HINTS.md).

**"Tags not detected"**: Put `tags:` directly on each task, not only on a block.

**`make test` fails with "No module named pytest"**: Run `make setup` first — it creates the Python virtual environment.

**Need a clean slate**: `make reset` destroys and rebuilds all nodes; `make destroy` tears everything down.
