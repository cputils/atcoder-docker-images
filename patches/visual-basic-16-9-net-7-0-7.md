# Visual Basic 16.9 (.NET 7.0.7)

## Summary
Install .NET SDK 7.0.304 on Ubuntu 24.04 without the Microsoft Ubuntu APT repository.

## Changes
- Replaced the Ubuntu 22.10 Microsoft APT repository setup with `dotnet-install.sh`.
- Installed the SDK into `/usr/share/dotnet` and linked `dotnet` into `/usr/local/bin`.
- Installed the native libraries required by the .NET SDK.

## Notes
- The Microsoft repository's `dotnet-sdk-7.0.304` package requires `netstandard-targeting-pack-2.1`, which is unavailable in the repository.
