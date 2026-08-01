#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys

from build import (
    DEFAULT_INFO_DIR,
    DEFAULT_TAG,
    load_targets,
    normalize_tag_component,
    resolve_target,
)


def resolve_from_git_remote() -> tuple[str, str]:
    try:
        completed = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return "", ""

    remote = completed.stdout.strip()
    if not remote:
        return "", ""

    remote.removesuffix(".git")

    prefix = "https://github.com/"
    if remote.startswith(prefix):
        owner_repo = remote[len(prefix) :]
        if "/" in owner_repo:
            owner, repo = owner_repo.split("/", 1)
            return owner, repo

    scp_prefix = "git@github.com:"
    if remote.startswith(scp_prefix):
        owner_repo = remote[len(scp_prefix) :]
        if "/" in owner_repo:
            owner, repo = owner_repo.split("/", 1)
            return owner, repo

    return "", ""


def _gh_run(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["gh", *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError, FileNotFoundError:
        return ""


def resolve_owner_repo() -> tuple[str, str]:
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    env_owner = ""
    env_repo = ""
    if "/" in repository:
        env_owner, env_repo = repository.split("/", 1)
    git_owner, git_repo = resolve_from_git_remote()

    resolved_owner = env_owner or git_owner
    resolved_repo = env_repo or git_repo

    if not resolved_owner or not resolved_repo:
        raise SystemExit(
            "Unable to resolve GHCR namespace. Set GITHUB_REPOSITORY,"
            " or configure remote.origin.url."
        )

    return resolved_owner.casefold(), resolved_repo.casefold()


def resolve_credentials() -> tuple[str, str]:
    resolved_username = os.environ.get("GHCR_USERNAME") or os.environ.get(
        "GITHUB_ACTOR"
    )
    resolved_token = os.environ.get("GHCR_TOKEN") or os.environ.get("GITHUB_TOKEN")

    if not resolved_username:
        print("GITHUB_ACTOR not set, falling back to GitHub CLI...")
        resolved_username = _gh_run(["api", "user", "--jq", ".login"])

    if not resolved_token:
        print("GITHUB_TOKEN not set, falling back to GitHub CLI...")
        resolved_token = _gh_run(["auth", "token"])

    if not resolved_username or not resolved_token:
        raise SystemExit(
            "Missing GHCR credentials. Set GHCR_USERNAME+GHCR_TOKEN"
            " (or GITHUB_ACTOR+GITHUB_TOKEN), or run `gh auth login`."
        )

    return resolved_username, resolved_token


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def docker_login(username: str, token: str) -> None:
    """Log in to ghcr.io by piping the token through stdin."""
    subprocess.run(
        ["docker", "login", "ghcr.io", "--username", username, "--password-stdin"],
        check=True,
        input=token,
        text=True,
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("usage: upload_built_package.py SELECTOR")

    selector = args[0]
    targets = load_targets(DEFAULT_INFO_DIR)
    target = resolve_target(selector, targets)

    normalized_stem = normalize_tag_component(target.stem)
    source_image = f"{normalized_stem}:{DEFAULT_TAG}"
    owner, repo = resolve_owner_repo()
    target_image = f"ghcr.io/{owner}/{repo}/{normalized_stem}:{DEFAULT_TAG}"

    print(f"selector: {selector}")
    print(f"source:   {source_image}")
    print(f"target:   {target_image}")

    username, token = resolve_credentials()
    docker_login(username, token)
    run(["docker", "image", "inspect", source_image])
    run(["docker", "tag", source_image, target_image])
    run(["docker", "push", target_image])

    print(f"pushed:   {target_image}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
