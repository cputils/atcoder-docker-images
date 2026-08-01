# Julia (1.11.6)

## Summary
Make the `install` step find Julia from both runner and root Juliaup locations.

## Changes
- Extended the PATH export to include `/home/runner/.juliaup/bin` and `/root/.juliaup/bin`.

## Notes
- This preserves the original runner path and adds the location used during Docker builds.
