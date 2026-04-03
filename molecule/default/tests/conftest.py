"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for Compliance verification.
"""
import os
import pytest
import sys

_COLOR = (
    os.environ.get("ARIA_COLOR") == "1"
    or (hasattr(sys.stderr, "isatty") and sys.stderr.isatty())
)


def _c(code):
    return code if _COLOR else ""


GREEN = _c("\033[32m")
RED = _c("\033[31m")
YELLOW = _c("\033[33m")
CYAN = _c("\033[36m")
DIM = _c("\033[2m")
BOLD = _c("\033[1m")
RESET = _c("\033[0m")

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


class _ARIAReporter:
    def __init__(self):
        self._current_class = None
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self._phase_results = {}
        self._current_phase_passed = True

    @staticmethod
    def _out(text):
        sys.stderr.write(text)
        sys.stderr.flush()

    def record(self, nodeid, outcome, longrepr):
        parts = nodeid.split("::")
        cls = parts[1] if len(parts) > 1 else ""
        test = parts[-1]

        num, label = PHASES.get(cls, ("?", "Unknown"))
        name = FRIENDLY.get(test, test)

        if cls != self._current_class:
            if self._current_class is not None:
                self._phase_results[self._current_class] = self._current_phase_passed
            self._current_phase_passed = True
            self._current_class = cls
            self._out(f"\n  {CYAN}{BOLD}Phase {num}: {label}{RESET}\n")

        if outcome != "passed":
            self._current_phase_passed = False

        if outcome == "passed":
            self.passed += 1
            self._out(f"    {GREEN}\u2713{RESET} {name}\n")
        elif outcome == "skipped":
            self.skipped += 1
            self._out(f"    {YELLOW}\u25cb{RESET} {DIM}{name} \u2014 skipped{RESET}\n")
        else:
            self.failed += 1
            hint = _extract_hint(longrepr)
            if hint:
                self._out(f"    {YELLOW}\u2717{RESET} {name}\n")
                self._out(f"      {DIM}\u21b3 {hint}{RESET}\n")
            else:
                self._out(f"    {RED}\u2717{RESET} {name}\n")

    def summary(self):
        if self._current_class is not None:
            self._phase_results[self._current_class] = self._current_phase_passed

        total = self.passed + self.failed + self.skipped
        self._out(f"\n  {'\u2500' * 44}\n")

        phases_complete = sum(1 for v in self._phase_results.values() if v)
        total_phases = len(PHASES)
        self._out(f"  {BOLD}Progress:{RESET} {phases_complete} of {total_phases} phases complete\n")

        parts = []
        if self.passed:
            parts.append(f"{GREEN}{self.passed} verified{RESET}")
        if self.failed:
            parts.append(f"{RED}{self.failed} deficient{RESET}")
        if self.skipped:
            parts.append(f"{YELLOW}{self.skipped} skipped{RESET}")
        self._out(
            f"  {BOLD}Results:{RESET} {' \u00b7 '.join(parts)}"
            f"  {DIM}({total} checks){RESET}\n"
        )


def _extract_hint(longrepr):
    if longrepr is None:
        return None
    crash = getattr(longrepr, "reprcrash", None)
    if crash:
        msg = getattr(crash, "message", "")
        if "ARIA:" in msg:
            return msg.split("ARIA:", 1)[-1].strip()
    text = str(longrepr)
    if "ARIA:" in text:
        raw = text.split("ARIA:")[-1].splitlines()[0].strip()
        return raw.rstrip("'\"")
    return None


_reporter = _ARIAReporter()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == "call":
        _reporter.record(report.nodeid, report.outcome, report.longrepr)
        report.longrepr = None
    elif report.when == "setup" and report.skipped:
        _reporter.record(report.nodeid, "skipped", report.longrepr)
        report.longrepr = None


def pytest_report_teststatus(report, config):
    if report.when == "call":
        return report.outcome, "", ""
    if report.when == "setup" and report.skipped:
        return "skipped", "", ""


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    _reporter.summary()
    terminalreporter.stats.pop("failed", None)
    terminalreporter.stats.pop("error", None)
