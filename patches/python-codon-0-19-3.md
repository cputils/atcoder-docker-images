# Python (Codon 0.19.3)

## Summary
Install `locales` so the final `locale-gen` step can run successfully.

## Changes
- Added `locales` to the dependency install step before the script calls `sudo locale-gen en_US.UTF-8`.

## Notes
- The rest of the Codon setup is unchanged.
- This keeps the original script flow intact while providing the missing command.
