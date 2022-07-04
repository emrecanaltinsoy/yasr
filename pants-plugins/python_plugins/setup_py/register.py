# Copyright 2020 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
from typing import List
from packaging.version import Version, parse
from pants.backend.python.goals.setup_py import SetupKwargs, SetupKwargsRequest
from pants.engine.fs import DigestContents, GlobMatchErrorBehavior, PathGlobs
from pants.engine.rules import Get, collect_rules, rule
from pants.engine.target import Target
from pants.engine.unions import UnionRule


def __get_target_dir_from_spec(path_safe_spec: str) -> str:
    path = path_safe_spec.split(".")[:-1]
    return "/".join(path)


def __get_version_from_local_file(digest_contents: List[DigestContents]) -> str:
    package_version = [
        file_content.content.decode() for file_content in digest_contents
    ][0]
    package_version = [char for char in package_version.split("\n")][0]
    package_version = parse(package_version)
    return package_version.base_version


class PythonSetupKwargsRequest(SetupKwargsRequest):
    @classmethod
    def is_applicable(cls, _: Target) -> bool:
        # We always use our custom `setup()` kwargs generator for `python_distribution` targets in
        # this repo.
        return True


@rule
async def python_setup_kwargs(request: PythonSetupKwargsRequest) -> SetupKwargs:
    kwargs = request.explicit_kwargs.copy()
    target_dir = __get_target_dir_from_spec(request.target.address.path_safe_spec)
    if not target_dir:
        raise Exception("Empty target address.")
    digest_contents = await Get(
        DigestContents,
        PathGlobs(
            [f"{target_dir}/**/.version"],
            description_of_origin="Python version file",
            glob_match_error_behavior=GlobMatchErrorBehavior.error,
        ),
    )
    package_version = __get_version_from_local_file(digest_contents)
    # Hardcode certain kwargs and validate that they weren't already set.
    default_kwargs = dict(
        version=package_version,
        long_description_content_type="text/markdown",
        zip_safe=True,
    )
    conflicting_hardcoded_kwargs = set(kwargs.keys()).intersection(
        default_kwargs.keys()
    )
    if conflicting_hardcoded_kwargs:
        raise ValueError(
            f"These kwargs should not be set in the `provides` field for {request.target.address} "
            "because Pants's internal plugin will automatically set them: "
            f"{sorted(conflicting_hardcoded_kwargs)}"
        )
    kwargs.update(default_kwargs)

    return SetupKwargs(kwargs, address=request.target.address)


def rules():
    return (*collect_rules(), UnionRule(SetupKwargsRequest, PythonSetupKwargsRequest))
