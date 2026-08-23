"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for Compliance verification.
"""
import os
import pytest
import sys

PHASES = {
    "TestObstacleCourse1":   ("1", "Compliance Range — Mission 1 (Write the Role)"),
    "TestObstacleCourse2":   ("2", "Compliance Range — Mission 2 (Write the Tests)"),
    "TestMainMission":       ("3", "Main Mission — Compliance as Code"),
}

FRIENDLY = {
    "test_oc1_role_exists":                "Role cis_hardening exists",
    "test_oc1_tasks_have_content":         "tasks/main.yml has CIS tasks",
    "test_oc1_tasks_are_tagged":           "Tasks use CIS control tags",
    "test_oc1_role_applied_successfully":  "Role applied to cis-target",
    "test_oc1_tests_pass":                 "All 8 pre-written CIS tests pass",
    "test_oc2_test_file_exists":           "test_compliance_baseline.py exists",
    "test_oc2_tests_have_assertions":      "Tests have meaningful assertions",
    "test_oc2_role_applied":               "Compliance baseline applied to cis-target",
    "test_oc2_tests_catch_bug":            "Tests detect compliance gaps",
    "test_mm_role_exists":                 "fleet_hardening role exists",
    "test_mm_site_yml_exists":             "site.yml references role",
    "test_mm_tasks_are_tagged":            "Role tasks use CIS tags",
    "test_mm_test_file_exists":            "Test file with 10+ checks",
    "test_mm_compliance_report":           "COMPLIANCE.md has data",
    "test_mm_tests_pass":                  "Tests pass against fleet",
}

# The phase-oriented summary is rendered by the shared `aria-reporter`
# pytest plugin (installed via requirements.txt); this file only declares
# the mission's phases + friendly objective names.
from aria_reporter import configure  # noqa: E402

configure(phases=PHASES, friendly=FRIENDLY, mission_id="2-2")
