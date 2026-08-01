# Whitespace (whitespacers 1.3.0)

## Summary
Install Rust with temporary Cargo and Rustup homes so `cargo install` can run cleanly in the container build.

## Changes
- Added `CARGO_HOME` and `RUSTUP_HOME` exports before the Rust toolchain install.
- Switched from the distro `rustup` package to the upstream installer.
- Copied `wsc` from the temporary Cargo home instead of `$HOME/.cargo`.
- Removed the temporary Cargo and Rustup directories after installation.

## Notes
- This keeps the original compiler choice and version pin intact.
