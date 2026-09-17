# Mission 2.2: Compliance as Code — Hints

> 📚 Deeper reference: [FM-4 — CIS & Compliance Reference](https://github.com/starfall-defence-corps/sdc-academy/blob/main/field-manuals/FM-4-cis-compliance-reference.md)

> Back to: [Briefing](BRIEFING.md) | [Exercises](EXERCISES.md) | [Checklist](../CHECKLIST.md)

## Troubleshooting

**SSH issues**: Run `make setup` first. Check `docker ps` to verify containers are running.

**Lynis not found**: Lynis is pre-installed in all containers. If missing, install with: `ansible cis-target -m apt -a "name=lynis state=present"`

**sysctl errors in Docker**: Some sysctl parameters can't be set in Docker containers. Use `ignore_errors: true` for those, or check if the parameter exists first with `when`.

**Testinfra connection issues**: Ensure you're using the correct port. cis-target is 2251, fleet nodes are 2221-2223.

**Tags not detected**: ARIA checks that at least 3 tasks have `tags:` in your YAML. Make sure you're using the tags keyword directly on each task, not just in a block.

**Need a clean slate**: Run `make reset` to rebuild containers. Your workspace files are preserved.

## Sprint Triage — Running Controls Fleet-Wide by Priority

The main mission is timed (H-45). Tags let you push one priority tier to the whole fleet in a single command, then move to the next — this is the point of tagging every task:

```bash
# P1 — credential defence, all nodes first
ansible-playbook -i workspace/main-mission/inventory/hosts.yml workspace/main-mission/site.yml --tags cis_5_2

# P2 — surface & persistence
ansible-playbook -i workspace/main-mission/inventory/hosts.yml workspace/main-mission/site.yml --tags cis_5_1,cis_3_3

# P3 — evidence & hygiene
ansible-playbook -i workspace/main-mission/inventory/hosts.yml workspace/main-mission/site.yml --tags cis_6_1,cis_1_5,cis_1_7

# Out of time? Confirm at least P1 landed everywhere:
ansible all -i workspace/main-mission/inventory/hosts.yml -m shell -a \
  "sshd -T | grep -E 'permitrootlogin|passwordauthentication|maxauthtries'" --become
```

**Wide before deep**: if the clock beats you, P1 on all three nodes beats P1–P3 on one node. See [BRIEFING §3f](BRIEFING.md) for the full priority table and the reasoning behind the order.

## Common CIS Implementation Patterns

### sysctl

```yaml
- name: "CIS 3.x — Kernel parameter"
  ansible.posix.sysctl:
    name: net.ipv4.conf.all.accept_redirects
    value: "0"
    sysctl_set: true
    reload: true
  tags: [cis_3_3]
```

### File permissions

```yaml
- name: "CIS 6.1.3 — Shadow file permissions"
  ansible.builtin.file:
    path: /etc/shadow
    mode: "0640"
  tags: [cis_6_1]
```

### Limits

```yaml
- name: "CIS 1.5.1 — Restrict core dumps"
  ansible.builtin.copy:
    content: "* hard core 0\n"
    dest: /etc/security/limits.d/cis.conf
    mode: "0644"
  tags: [cis_1_5]
```
