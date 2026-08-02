# Fix (1.1.0-alpha.12)

## Summary
Resolve the compiler-compatible `ring-buffer` version before `cp-library`.

## Changes
- Moved the pinned `ring-buffer` 0.1.1 dependency before `cp-library`.

## Notes
- Resolving `cp-library` first selects `ring-buffer` 0.1.2, which uses APIs unsupported by Fix 1.1.0-alpha.12.
