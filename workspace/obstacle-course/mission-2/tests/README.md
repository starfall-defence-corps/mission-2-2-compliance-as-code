# Obstacle Course — Mission 2: Write the Tests

The `compliance_baseline` role has been applied. It claims to implement CIS controls. But it has **bugs** — controls that are misconfigured or missing entirely.

## Your Task

Write `test_compliance_baseline.py` in this directory.

### Required Tests

1. **Basic checks** (should pass):
   - SSH service is running
   - Login banner exists at `/etc/issue.net`
   - `cron.allow` exists with correct permissions

2. **Compliance checks** (some should fail — that's the point):
   - SSH MaxAuthTries is 4 or less (CIS 5.2.7)
   - `/etc/shadow` permissions are 0640 (CIS 6.1.3)
   - ICMP redirects are rejected (CIS 3.3.2)
   - Core dumps are restricted (CIS 1.5.1)

### Run Your Tests

Run from the project root:

```bash
pytest workspace/obstacle-course/mission-2/tests/test_compliance_baseline.py \
  --hosts=ssh://cadet@localhost:2251 \
  --ssh-identity-file=workspace/.ssh/cadet_key \
  --ssh-config=workspace/.ssh/testinfra_ssh_config \
  --sudo -v
```

Failing tests prove the bugs exist. You are **not** fixing the role — you are proving the problems are there.
