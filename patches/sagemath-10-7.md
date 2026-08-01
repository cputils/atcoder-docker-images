# SageMath (10.7)

## Summary
Allow SageMath to configure inside the root-owned Docker build environment and use the system primecount library.

## Changes
- Added `--enable-build-as-root` to the Sage `./configure` command.
- Installed `libprimecount-dev` so Sage detects the system `primecount` package instead of building it from source.

## Notes
- This matches the container build context used by this repository, avoids Sage's root-user guard, and skips the expensive `primecount` source build.
