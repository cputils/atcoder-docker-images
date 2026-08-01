# atcoder-docker-images

Docker images for AtCoder language environments.

## Use a published image

1. Pick the selector for the language you want. The safest choice is the `info/*.toml` filename stem.
2. Pull the image:

```bash
docker pull ghcr.io/cputils/atcoder-docker-images/<normalized-stem>:2025-10
```

3. Run it with your source mounted into `/judge`:

```bash
docker run --rm -it -v "$PWD:/judge" ghcr.io/cputils/atcoder-docker-images/<normalized-stem>:2025-10 bash
```

Inside the container, work in `/judge` and use the language tools directly.

## What is included

Each image is built by running the `install` step in its metadata file. Common pieces include:

- Base image: `ubuntu:24.04`
- Shared packages: `bash`, `curl`, `git`, `python3`, `build-essential`, and more
- Working directory: `/judge`
- Metadata: `/opt/atcoder/info.toml`
- Install script: `/opt/atcoder/atcoder-install.sh`
- Default shell at runtime: `bash`

## Metadata file

Each image is defined by one `info/*.toml` file. That file is the source of truth for the image and usually contains:

- `language`: a short language name
- `display`: the user-facing name shown in selectors
- `install`: the build-time setup script
- `compile`: the compile check or command, when present
- `execution`: the runtime command, when present
- `filename`: the main source filename expected by the runtime, when present
- `license` and `library`: dependency metadata, when present

If you are choosing an image, start with the filename stem under `info/`, then check the `display` field when needed.

## About `patches/`

`patches/` contains short notes for images that need extra handling. The patch filename matches the image stem, and each file names its target language:

If a language has a patch file, read it before using that image.

## Build locally (optional)

```bash
uv run build.py python-cpython-3-13-7
```

`selector` can be any of:

- the `info/*.toml` filename stem
- the `language` field
- the `display` field

Examples:

```bash
uv run build.py "Python"
uv run build.py "Python (CPython 3.13.7)"
uv run build.py python-cpython-3-13-7
```

The local tag after building is `"<normalized-stem>:2025-10"`.
For example, `python-cpython-3-13-7` becomes `python-cpython-3-13-7:2025-10`.

### Run the container after building

```bash
docker run --rm -it python-cpython-3-13-7:2025-10 bash
```

The working directory is `/judge`. Put your source files there and use tools like `python` and `g++` directly.

## Publish to GHCR

This is only needed if you are publishing a new image.

```bash
uv run upload.py python-cpython-3-13-7
```

`upload.py` resolves the GHCR namespace in this order:

1. `GITHUB_REPOSITORY`
2. `remote.origin.url`

It accepts credentials from either:

- `GHCR_USERNAME` + `GHCR_TOKEN`
- `GITHUB_ACTOR` + `GITHUB_TOKEN`

If neither is set, it falls back to the `gh` CLI.

The full pushed image reference is:

```text
ghcr.io/cputils/atcoder-docker-images/<normalized-stem>:2025-10
```

## GitHub Actions

Two workflows are included:

- `build-and-upload-language.yml`
  - builds and uploads one selector
- `build-and-upload-all-languages.yml`
  - builds and uploads all languages
  - supports `skip_selectors` to exclude specific images
