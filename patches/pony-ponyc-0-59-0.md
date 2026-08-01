# Pony (ponyc 0.59.0)

## Summary
Replace the failing `ponyup` download flow with source builds for `ponyc` and `corral`.

## Changes
- Built `ponyc` from source using `0.59.0`.
- Built `corral` from source using `0.9.2`.
- Added strict shell mode and temporary build directory cleanup.
- Updated the compile PATH to use `/usr/local/bin`.

## Notes
- The Cloudsmith package download could return an empty body, which caused checksum mismatches.
