# Scala (Dotty 3.7.2)

## Summary
Keep the library build on sbt 1.x and install Scala CLI from its release binary.

## Changes
- Pinned sbt to `1.11.6`.
- Installed Scala CLI 1.9.1 from its release binary.

## Notes
- The required plugins are not published for sbt 2.x.
- The Scala CLI package repository signing key changed, so the original APT installation no longer succeeds.
