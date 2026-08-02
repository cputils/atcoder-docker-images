# Jule (0.1.6)

## Summary
Use the official LLVM distribution, skip installation-only tests, update the LightGBM fetch path, and reduce resource usage during installation.

## Changes
- Replaced the local LLVM source build with the official LLVM 21.1.0 Linux X64 distribution.
- Streamed the LLVM archive directly into `/usr/local` without storing a temporary copy.
- Excluded MLIR, Flang, LLDB, and BOLT components that were not enabled by the original installation script.
- Built only LLVM libc and OpenMP from the matching 21.1.0 source because they are not included in the official distribution.
- Disabled Abseil tests during image installation.
- Removed downloaded archives, source trees, and build trees after their installed files were copied.
- Switched the LightGBM release download owner to `lightgbm-org`.
- Updated the extracted source directory path to `lightgbm-org-LightGBM`.
- Updated the LightGBM license URL to the new repository.
- Disabled parallel building of OR-Tools.

## Notes
- Building LLVM and its runtimes from source exceeded the two-hour CI job limit before the remaining libraries could be installed.
- The excluded LLVM components reduce the extracted distribution by about 3.8 GiB on the 14 GB hosted runner.
- The official distribution keeps LLVM, Clang, LLD, Polly, compiler-rt, libc++, libc++abi, and libunwind at 21.1.0.
- Abseil tests increase peak resource usage and are not required to install the library.
- Cleanup is performed only after installation and does not remove installed files.
- `microsoft/LightGBM` now serves redirect metadata, so the old download path no longer fetches the source tarball correctly.
