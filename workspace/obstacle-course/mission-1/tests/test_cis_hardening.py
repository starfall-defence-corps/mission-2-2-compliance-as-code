"""CIS Level 1 Hardening Tests — Obstacle Course Mission 1.

These 8 tests define the specification. Your role must make them all pass.
Each test maps to a CIS benchmark control.
"""


def test_ssh_max_auth_tries(host):
    """CIS 5.2.7: SSH MaxAuthTries must be 4 or less."""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.exists
    assert sshd.contains("MaxAuthTries 4")


def test_ssh_login_grace_time(host):
    """CIS 5.2.16: SSH LoginGraceTime must be 60 seconds or less."""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.contains("LoginGraceTime 60")


def test_ssh_client_alive(host):
    """CIS 5.2.13: SSH idle timeout must be configured."""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.contains("ClientAliveInterval 300")
    assert sshd.contains("ClientAliveCountMax 3")


def test_shadow_file_permissions(host):
    """CIS 6.1.3: /etc/shadow must have restricted permissions."""
    shadow = host.file("/etc/shadow")
    assert shadow.exists
    assert shadow.mode == 0o640


def test_core_dumps_restricted(host):
    """CIS 1.5.1: Core dumps must be restricted."""
    limits = host.file("/etc/security/limits.d/cis.conf")
    assert limits.exists
    assert limits.contains("* hard core 0")


def test_sysctl_network_hardened(host):
    """CIS 3.3.2: ICMP redirects must not be accepted."""
    result = host.run("sysctl net.ipv4.conf.all.accept_redirects")
    assert "= 0" in result.stdout


def test_login_banner_exists(host):
    """CIS 1.7.1: A warning banner must be configured."""
    issue = host.file("/etc/issue.net")
    assert issue.exists
    content = issue.content_string
    assert len(content.strip()) > 10, "Banner must contain a meaningful warning message"


def test_cron_access_restricted(host):
    """CIS 5.1.8: cron must be restricted to authorised users."""
    cron_allow = host.file("/etc/cron.allow")
    assert cron_allow.exists
    assert cron_allow.user == "root"
    assert cron_allow.mode == 0o600
