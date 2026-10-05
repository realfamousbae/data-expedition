# Security policy

Data Expedition is a set of instructions (a skill in the open Agent Skills format, usable in Claude Code, Codex, Gemini CLI, Cursor, Copilot and other agents) plus a small build script. It contains no runtime service,
but security still matters: the skill guides an agent that can read files, run commands, and browse the web.

## What counts as a security issue

- Wording in `SKILL.md` or `references/` that could lead an agent to cross its boundaries: modify or exfiltrate data
  without being asked, follow instructions embedded in files or web pages, bypass paywalls, logins, or other access
  controls, or collect personal data about private individuals.
- Vulnerabilities in `scripts/` or in the CI workflow (for example unsafe file handling or workflow permissions).
- Secrets, tokens, or personal data committed to the repository.

General model behavior (hallucinations, refusals, quality problems) is not a security issue; please open a normal issue.

## Reporting

Please report privately rather than in a public issue:

1. Use **Security, Report a vulnerability** on the repository page (GitHub private vulnerability reporting), if it is
   enabled.
2. Otherwise open a minimal public issue that says you have a security report, with no details, and ask for a private
   channel.

Include the affected file and lines, what an agent could be induced to do, and a way to reproduce it. You can expect an
acknowledgement within a few days and a fix or a clear decision within a reasonable time.

## Supported versions

Only the latest release receives fixes.
