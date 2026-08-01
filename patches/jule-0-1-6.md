# Jule (0.1.6)

## Summary
Update the LightGBM fetch path and cap Jule build jobs.

## Changes
- Switched the LightGBM release download owner to `lightgbm-org`.
- Updated the extracted source directory path to `lightgbm-org-LightGBM`.
- Updated the LightGBM license URL to the new repository.
- Changed the LLVM build to use `LLVM_PARALLEL_LINK_JOBS=1`.
- Disable parallel building of OR-Tools.

## Notes
- `microsoft/LightGBM` now serves redirect metadata, so the old download path no longer fetches the source tarball correctly.
