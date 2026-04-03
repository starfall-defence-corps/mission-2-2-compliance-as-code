# Starfall Defence Corps Academy

## Mission 2.2: Compliance as Code

> *"Captain Unpatched hasn't updated a server since 2019. 'If it works, don't touch it.' His compliance evidence is a screenshot from three years ago. This ends now."*

You are a Lieutenant JG at the Starfall Defence Corps Academy. You can harden systems. You can test them. Now prove you can measure compliance against an industry standard — CIS Benchmarks — and implement it as code.

## Prerequisites

- Completed Module 1 (Missions 1.1–1.5 + Gateway Simulation)
- Completed Mission 2.1 (Weapon Handling Test)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
git clone https://github.com/YOUR-USERNAME/mission-2-2-compliance-as-code.git
cd mission-2-2-compliance-as-code
make setup
source venv/bin/activate
```

Read your orders: [Mission Briefing](docs/BRIEFING.md)

## Lab Architecture

```
 Compliance Range              Fleet
+------------------+    +----------------------------------+
| cis-target :2251 |    | sdc-web   :2221  (Ubuntu 22.04) |
| Ubuntu 22.04     |    | sdc-db    :2222  (Rocky Linux 9) |
| CIS violations   |    | sdc-comms :2223  (Ubuntu 22.04) |
+------------------+    +----------------------------------+
```

## Mission Structure

| Part | Description | Location |
|------|-------------|----------|
| Obstacle Course 1 | Given CIS tests, write the role | `workspace/obstacle-course/mission-1/` |
| Obstacle Course 2 | Given buggy role, write tests | `workspace/obstacle-course/mission-2/` |
| Main Mission | CIS-harden the fleet with Lynis | `workspace/main-mission/` |

## Available Commands

```
make help          Show available commands
make setup         Launch compliance range + fleet (4 containers)
make test          Ask ARIA to verify your work
make reset         Destroy and rebuild all nodes
make destroy       Tear down everything
make ssh-cis-target SSH into obstacle course target
make ssh-web       SSH into sdc-web (fleet)
make ssh-db        SSH into sdc-db (fleet)
make ssh-comms     SSH into sdc-comms (fleet)
```

## ARIA Review (Pull Request Workflow)

**Locally** — run `make test` for instant verification.

**On Pull Request** — push your work, open a PR, ARIA reviews automatically.

To enable PR reviews, add `ANTHROPIC_API_KEY` to your repo's Secrets.
