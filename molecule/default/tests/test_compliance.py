"""
=== STARFALL DEFENCE CORPS ACADEMY ===
ARIA Automated Verification — Mission 2.2: Compliance as Code
================================================================
"""
import ast
import os
import re
import subprocess
import yaml
import pytest


def _root_dir():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(tests_dir, "..", "..", ".."))


def _workspace_dir():
    return os.path.join(_root_dir(), "workspace")


def _oc_dir(mission):
    return os.path.join(_workspace_dir(), "obstacle-course", f"mission-{mission}")


def _mm_dir():
    return os.path.join(_workspace_dir(), "main-mission")


def _run_cmd(*args, cwd=None, timeout=90):
    return subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd or _workspace_dir(),
    )


def _run_ansible(*args, cwd=None, timeout=90):
    return _run_cmd(*args, cwd=cwd, timeout=timeout)


def _count_test_functions(filepath):
    """Count test_ functions in a Python file using AST parsing."""
    try:
        with open(filepath) as f:
            tree = ast.parse(f.read())
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                count += 1
        return count
    except (SyntaxError, FileNotFoundError):
        return 0


def _count_assertions(filepath):
    """Count assert statements in a Python file."""
    try:
        with open(filepath) as f:
            content = f.read()
        return content.count("assert ")
    except FileNotFoundError:
        return 0


def _tasks_have_tags(tasks_file):
    """Check if tasks in a YAML file use tags."""
    try:
        with open(tasks_file) as f:
            data = yaml.safe_load(f)
        if not data or not isinstance(data, list):
            return False
        tagged = sum(1 for task in data if isinstance(task, dict) and "tags" in task)
        return tagged >= 3
    except (FileNotFoundError, yaml.YAMLError):
        return False


# -------------------------------------------------------------------
# Phase 1: Obstacle Course — Mission 1 (Write the Role)
# -------------------------------------------------------------------

class TestObstacleCourse1:
    """ARIA verifies: Has the cadet written a CIS hardening role?"""

    def test_oc1_role_exists(self):
        """cis_hardening role must exist"""
        role_dir = os.path.join(_oc_dir(1), "roles", "cis_hardening")
        assert os.path.isdir(role_dir), (
            "ARIA: No role at obstacle-course/mission-1/roles/cis_hardening/. "
            "Create it with: ansible-galaxy init roles/cis_hardening"
        )

    def test_oc1_tasks_have_content(self):
        """tasks/main.yml must have CIS hardening tasks"""
        role_dir = os.path.join(_oc_dir(1), "roles", "cis_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        tasks = os.path.join(role_dir, "tasks", "main.yml")
        assert os.path.isfile(tasks), (
            "ARIA: tasks/main.yml not found in cis_hardening role."
        )
        with open(tasks) as f:
            data = yaml.safe_load(f)
        assert data and isinstance(data, list) and len(data) >= 5, (
            "ARIA: tasks/main.yml needs at least 5 tasks. "
            "Read the 8 tests — each one tells you what the role must do."
        )

    def test_oc1_tasks_are_tagged(self):
        """Tasks must use CIS control tags"""
        role_dir = os.path.join(_oc_dir(1), "roles", "cis_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        tasks = os.path.join(role_dir, "tasks", "main.yml")
        if not os.path.isfile(tasks):
            pytest.skip("tasks/main.yml not found")
        assert _tasks_have_tags(tasks), (
            "ARIA: Tasks must use CIS control tags (e.g., tags: [cis_5_2]). "
            "Tags enable selective enforcement: ansible-playbook --tags cis_5_2"
        )

    def test_oc1_role_applied_successfully(self):
        """Role must be applied to cis-target without errors"""
        role_dir = os.path.join(_oc_dir(1), "roles", "cis_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible-playbook", "-i", "inventory.yml", "site.yml",
            cwd=_oc_dir(1),
            timeout=120,
        )
        assert result.returncode == 0, (
            f"ARIA: Playbook failed:\n{result.stderr[:500]}"
        )

    def test_oc1_tests_pass(self):
        """All 8 pre-written CIS tests must pass"""
        role_dir = os.path.join(_oc_dir(1), "roles", "cis_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        ssh_key = os.path.join(_workspace_dir(), ".ssh", "cadet_key")
        result = _run_cmd(
            "python3", "-m", "pytest",
            os.path.join(_oc_dir(1), "tests", "test_cis_hardening.py"),
            f"--hosts=ssh://cadet@localhost:2251",
            f"--ssh-identity-file={ssh_key}",
            f"--ssh-config={os.path.join(_workspace_dir(), '.ssh', 'testinfra_ssh_config')}",
            "--sudo",
            "-v", "--tb=short",
            cwd=_oc_dir(1),
            timeout=60,
        )
        assert result.returncode == 0, (
            f"ARIA: {_count_failures(result.stdout)} of 8 tests failed. "
            "Read the test names — they tell you exactly what CIS control to fix."
        )


# -------------------------------------------------------------------
# Phase 2: Obstacle Course — Mission 2 (Write the Tests)
# -------------------------------------------------------------------

class TestObstacleCourse2:
    """ARIA verifies: Has the cadet written tests that catch compliance gaps?"""

    def test_oc2_test_file_exists(self):
        """test_compliance_baseline.py must exist in mission-2/tests/"""
        path = os.path.join(_oc_dir(2), "tests", "test_compliance_baseline.py")
        assert os.path.isfile(path), (
            "ARIA: No test file at obstacle-course/mission-2/tests/test_compliance_baseline.py. "
            "Write your Testinfra tests there."
        )

    def test_oc2_tests_have_assertions(self):
        """Tests must have meaningful assertions (at least 5)"""
        path = os.path.join(_oc_dir(2), "tests", "test_compliance_baseline.py")
        if not os.path.isfile(path):
            pytest.skip("Test file does not exist yet")
        count = _count_test_functions(path)
        assert count >= 5, (
            f"ARIA: Only {count} test function(s) found. Write at least 5 "
            "tests covering both basic checks and compliance verification."
        )

    def test_oc2_role_applied(self):
        """Compliance baseline role must be applied to cis-target"""
        result = _run_ansible(
            "ansible-playbook", "-i", "inventory.yml", "site.yml",
            cwd=_oc_dir(2),
            timeout=120,
        )
        assert result.returncode == 0, (
            f"ARIA: Compliance baseline role failed to apply:\n{result.stderr[:500]}"
        )

    def test_oc2_tests_catch_bug(self):
        """Student tests must detect at least one compliance gap"""
        path = os.path.join(_oc_dir(2), "tests", "test_compliance_baseline.py")
        if not os.path.isfile(path):
            pytest.skip("Test file does not exist yet")
        ssh_key = os.path.join(_workspace_dir(), ".ssh", "cadet_key")
        result = _run_cmd(
            "python3", "-m", "pytest",
            path,
            f"--hosts=ssh://cadet@localhost:2251",
            f"--ssh-identity-file={ssh_key}",
            f"--ssh-config={os.path.join(_workspace_dir(), '.ssh', 'testinfra_ssh_config')}",
            "--sudo",
            "-v", "--tb=short",
            cwd=_oc_dir(2),
            timeout=60,
        )
        has_passed = "passed" in result.stdout
        has_failed = "failed" in result.stdout or result.returncode != 0
        assert has_passed and has_failed, (
            "ARIA: Your tests should have a mix of passing tests (basic checks) "
            "and failing tests (catching compliance gaps). "
            "The compliance_baseline role has bugs — your tests should find them."
        )


# -------------------------------------------------------------------
# Phase 3: Main Mission — Compliance as Code
# -------------------------------------------------------------------

class TestMainMission:
    """ARIA verifies: Has the cadet built a CIS-compliant fleet?"""

    def test_mm_role_exists(self):
        """fleet_hardening role must exist"""
        role_dir = os.path.join(_mm_dir(), "roles", "fleet_hardening")
        assert os.path.isdir(role_dir), (
            "ARIA: No role at main-mission/roles/fleet_hardening/. "
            "Copy or recreate your role from Mission 1.5, then extend with CIS controls."
        )

    def test_mm_site_yml_exists(self):
        """site.yml must exist and reference the role"""
        path = os.path.join(_mm_dir(), "site.yml")
        assert os.path.isfile(path), (
            "ARIA: site.yml not found in main-mission/."
        )
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data and isinstance(data, list), (
            "ARIA: site.yml is empty or invalid."
        )

    def test_mm_tasks_are_tagged(self):
        """Role tasks must use CIS control tags"""
        role_dir = os.path.join(_mm_dir(), "roles", "fleet_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        tasks = os.path.join(role_dir, "tasks", "main.yml")
        if not os.path.isfile(tasks):
            pytest.skip("tasks/main.yml not found")
        assert _tasks_have_tags(tasks), (
            "ARIA: CIS tasks must be tagged. Use tags like cis_5_2, cis_6_1, etc. "
            "This enables selective enforcement with --tags."
        )

    def test_mm_test_file_exists(self):
        """Test file must exist with at least 10 test functions"""
        tests_dir = os.path.join(_mm_dir(), "tests")
        if not os.path.isdir(tests_dir):
            tests_dir = os.path.join(_mm_dir(), "molecule", "default", "tests")
        assert os.path.isdir(tests_dir), (
            "ARIA: No tests/ directory found. Create it with your Testinfra tests."
        )
        py_files = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
        assert len(py_files) >= 1, (
            "ARIA: No test_*.py files found in tests/."
        )
        total_tests = sum(_count_test_functions(os.path.join(tests_dir, f)) for f in py_files)
        assert total_tests >= 10, (
            f"ARIA: Only {total_tests} test function(s) found. You need at least 10 to cover "
            "SSH, firewall, MOTD, services, sysctl, permissions, and CIS controls."
        )

    def test_mm_compliance_report(self):
        """COMPLIANCE.md must exist with Lynis data"""
        path = os.path.join(_mm_dir(), "COMPLIANCE.md")
        assert os.path.isfile(path), (
            "ARIA: COMPLIANCE.md not found. Document your Lynis scores and CIS controls."
        )
        with open(path) as f:
            content = f.read()
        # Check that students filled in at least some data (not just the template)
        has_numbers = bool(re.search(r'\d{2,}', content))
        has_status = any(word in content.lower() for word in ["pass", "done", "implemented", "yes", "complete"])
        assert has_numbers or has_status, (
            "ARIA: COMPLIANCE.md appears to be the empty template. "
            "Fill in Lynis scores and control implementation status."
        )

    def test_mm_tests_pass(self):
        """Tests must pass against the fleet"""
        tests_dir = os.path.join(_mm_dir(), "tests")
        if not os.path.isdir(tests_dir):
            tests_dir = os.path.join(_mm_dir(), "molecule", "default", "tests")
        if not os.path.isdir(tests_dir):
            pytest.skip("No tests directory found")
        role_dir = os.path.join(_mm_dir(), "roles", "fleet_hardening")
        if not os.path.isdir(role_dir):
            pytest.skip("Role does not exist yet")
        # First apply the role
        inv_path = os.path.join(_mm_dir(), "inventory", "hosts.yml")
        if os.path.isfile(inv_path):
            apply_result = _run_ansible(
                "ansible-playbook", "-i", "inventory/hosts.yml", "site.yml",
                cwd=_mm_dir(),
                timeout=120,
            )
            if apply_result.returncode != 0:
                pytest.skip("Role failed to apply — fix it first")

        # Run student tests against fleet
        ssh_key = os.path.join(_workspace_dir(), ".ssh", "cadet_key")
        py_files = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
        test_paths = [os.path.join(tests_dir, f) for f in py_files]
        result = _run_cmd(
            "python3", "-m", "pytest",
            *test_paths,
            f"--hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223",
            f"--ssh-identity-file={ssh_key}",
            f"--ssh-config={os.path.join(_workspace_dir(), '.ssh', 'testinfra_ssh_config')}",
            "--sudo",
            "-v", "--tb=short",
            cwd=_mm_dir(),
            timeout=120,
        )
        assert result.returncode == 0, (
            "ARIA: Some of your tests failed against the fleet. "
            "Ensure your role works and your tests match the expected state."
        )


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _count_failures(pytest_output):
    """Extract failure count from pytest output."""
    match = re.search(r"(\d+) failed", pytest_output)
    return int(match.group(1)) if match else "some"
