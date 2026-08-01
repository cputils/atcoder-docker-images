# Ruby (3.3, TruffleRuby 25.0.0)

## Summary
Pin `rice` to `4.6.1` so `or-tools` and `torch-rb` continue to build with the older `From_Ruby(Arg*)` API.

## Changes
- Installed `rice` explicitly at `4.6.1` before the bulk gem installation.
- Switched the bulk install to `--conservative`.
- Updated the library metadata to record `rice` as explicitly managed.

## Notes
- The `4.7.x` series is incompatible with the current dependency set.
