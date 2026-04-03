# Mission 2.2: Compliance as Code — Checklist

## Phase 1: Understanding
- [ ] Read EXERCISES.md Phase 1
- [ ] Understand CIS control structure (ID, description, level)
- [ ] Understand Ansible tag concept

## Phase 2: Obstacle Course
- [ ] Mission 1: Read all 8 CIS tests
- [ ] Mission 1: Create cis_hardening role with tagged tasks
- [ ] Mission 1: All 8 tests pass
- [ ] Mission 2: Read the buggy compliance_baseline role
- [ ] Mission 2: Write test_compliance_baseline.py (5+ tests)
- [ ] Mission 2: Tests detect compliance gaps (mixed pass/fail)

## Phase 3: Main Mission
- [ ] Baseline Lynis scan recorded in COMPLIANCE.md
- [ ] fleet_hardening role extended with CIS controls
- [ ] All tasks tagged with CIS section IDs
- [ ] Role applied to fleet (3 nodes)
- [ ] Post-hardening Lynis scan shows improvement
- [ ] test_fleet_compliance.py with 10+ test functions
- [ ] Molecule scenario configured
- [ ] All tests pass against fleet
- [ ] COMPLIANCE.md complete
- [ ] `make test` — all phases pass
