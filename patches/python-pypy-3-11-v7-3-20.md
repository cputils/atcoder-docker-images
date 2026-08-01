# Python (PyPy 3.11-v7.3.20)

## Summary
Pin Meson below 1.11.0 so pandas can build from source during the PyPy image install step.

## Changes
- Added a pip constraint that keeps Meson below 1.11.0 for the isolated build environment used by `pip`.

## Notes
- This keeps the original install flow intact while avoiding the pandas/Meson 1.11 incompatibility.
