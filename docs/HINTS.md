# Mission 2.2: Compliance as Code — Hints

> Back to: [Briefing](BRIEFING.md) | [Exercises](EXERCISES.md) | [Checklist](../CHECKLIST.md)

## Troubleshooting

**SSH issues**: Run `make setup` first. Check `docker ps` to verify containers are running.

**Lynis not found**: Lynis is pre-installed in all containers. If missing, install with: `ansible cis-target -m apt -a "name=lynis state=present"`

**sysctl errors in Docker**: Some sysctl parameters can't be set in Docker containers. Use `ignore_errors: true` for those, or check if the parameter exists first with `when`.

**Testinfra connection issues**: Ensure you're using the correct port. cis-target is 2251, fleet nodes are 2221-2223.

**Tags not detected**: ARIA checks that at least 3 tasks have `tags:` in your YAML. Make sure you're using the tags keyword directly on each task, not just in a block.

**Need a clean slate**: Run `make reset` to rebuild containers. Your workspace files are preserved.

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
