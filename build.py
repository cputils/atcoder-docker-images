#!/usr/bin/env python3

from __future__ import annotations

import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_INFO_DIR = ROOT / "info"
DEFAULT_BASE_IMAGE = "ubuntu:24.04"
DEFAULT_TAG = "2025-10"
BASE_PACKAGES = [
    "bash",
    "ca-certificates",
    "curl",
    "git",
    "gnupg",
    "python3",
    "python3-pip",
    "sudo",
    "tar",
    "unzip",
    "wget",
    "xz-utils",
    "build-essential",
    "pkg-config",
]


@dataclass(frozen=True)
class MetadataTarget:
    path: Path
    payload: dict[str, Any]

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def language(self) -> str:
        value = self.payload.get("language")
        return value if isinstance(value, str) else ""

    @property
    def display(self) -> str:
        value = self.payload.get("display")
        return value if isinstance(value, str) else ""

    @property
    def install(self) -> str:
        value = self.payload.get("install")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{self.path} does not contain a non-empty install command"
            )
        return value

    def validate(self) -> None:
        _ = self.install


def normalize_selector(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def normalize_tag_component(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def load_targets(info_dir: Path) -> list[MetadataTarget]:
    if not info_dir.is_dir():
        raise FileNotFoundError(f"info directory not found: {info_dir}")

    targets: list[MetadataTarget] = []
    for path in sorted(info_dir.glob("*.toml")):
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"{path} must contain a TOML table")  # noqa
        targets.append(MetadataTarget(path=path, payload=payload))

    if not targets:
        raise FileNotFoundError(f"no TOML files found in {info_dir}")
    return targets


def _find_matches(
    selector: str,
    targets: list[MetadataTarget],
    *,
    normalize: bool,
) -> list[MetadataTarget]:
    transform = normalize_selector if normalize else str.casefold
    key = transform(selector)

    matches = []
    for target in targets:
        candidates: set[str] = {transform(target.stem)}
        if target.language:
            candidates.add(transform(target.language))
        if target.display:
            candidates.add(transform(target.display))
        if not normalize:
            candidates.add(target.stem)
        if key in candidates:
            matches.append(target)
    return matches


def resolve_target(selector: str, targets: list[MetadataTarget]) -> MetadataTarget:
    for normalize in (False, True):
        matches = _find_matches(selector, targets, normalize=normalize)
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError(_format_ambiguity(selector, matches))

    available = ", ".join(target.stem for target in targets)
    raise KeyError(
        f"unknown language selector: {selector}\navailable stems: {available}"
    )


def _format_ambiguity(selector: str, targets: list[MetadataTarget]) -> str:
    options = ", ".join(
        f"{target.stem} ({target.display or target.language})" for target in targets
    )
    return f"selector is ambiguous: {selector}\nuse an exact stem instead: {options}"


def write_build_context(
    build_dir: Path, target: MetadataTarget, *, base_image: str
) -> None:
    metadata_name = target.path.name
    metadata_dest = build_dir / metadata_name
    shutil.copy2(target.path, metadata_dest)

    install_script_name = "atcoder-install.sh"
    install_script = build_dir / install_script_name
    install_body = target.install.rstrip("\n")
    install_script.write_text(
        "#!/usr/bin/env bash\nset -e\n\n" + install_body + "\n",
        encoding="utf-8",
    )
    install_script.chmod(0o755)

    quoted_packages = " ".join(shlex.quote(pkg) for pkg in BASE_PACKAGES)

    dockerfile = build_dir / "Dockerfile"
    dockerfile.write_text(
        "\n".join(
            [
                f"FROM {base_image}",
                "ENV DEBIAN_FRONTEND=noninteractive",
                "ENV ATCODER=1",
                'SHELL ["/bin/bash", "-c"]',
                "RUN apt-get update && apt-get install -y --no-install-recommends "
                + quoted_packages
                + " && rm -rf /var/lib/apt/lists/*",
                "RUN mkdir -p /judge /opt/atcoder",
                "WORKDIR /judge",
                f"COPY {metadata_name} /opt/atcoder/info.toml",
                f"COPY {install_script_name} /opt/atcoder/{install_script_name}",
                "RUN apt-get update && ATCODER=1 /opt/atcoder/"
                + install_script_name
                + " && rm -rf /var/lib/apt/lists/*",
                'CMD ["bash"]',
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_image(context_dir: Path, tag: str) -> None:
    subprocess.run(["docker", "build", "-t", tag, str(context_dir)], check=True)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("usage: build_docker_image.py SELECTOR")

    selector = args[0]
    targets = load_targets(DEFAULT_INFO_DIR)
    target = resolve_target(selector, targets)
    image_tag = f"{normalize_tag_component(target.stem)}:{DEFAULT_TAG}"

    with tempfile.TemporaryDirectory(prefix="atcoder-docker-build-") as tmpdir:
        context_dir = Path(tmpdir)
        write_build_context(context_dir, target, base_image=DEFAULT_BASE_IMAGE)

        print(f"selector: {selector}")
        print(f"image:    {image_tag}")
        print(f"metadata: {target.path}")
        print(
            f"install:  {target.install.splitlines()[0] if target.install.splitlines() else ''}"
        )

        build_image(context_dir, image_tag)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
