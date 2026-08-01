# Eiffel (liberty-eiffel-07829e3)

## Summary
Fix the install failure in non-interactive CI by making the Liberty Eiffel bootstrap avoid TTY progress output and by ensuring the symlink target directory exists.

## Changes
- Set `plain=TRUE` before bootstrap.
- Created `/etc/xdg` explicitly with `sudo install -d /etc/xdg`.
- Replaced the symlink command with `sudo ln -sfn /usr/local/etc/xdg/liberty-eiffel /etc/xdg/liberty-eiffel`.

## Notes
- This makes the link step idempotent and compatible with `ubuntu:24.04`.
