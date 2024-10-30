import dagger

from dagger import Doc, DefaultPath, dag
from datetime import datetime
from typing import Annotated

from .tofu_context import TofuContext

class TofuJobs:
    _tofu_context: TofuContext

    def __init__(self, tofu_context: TofuContext):
        self._tofu_context = tofu_context

    async def format(self) -> str:
        """Check the code formatting"""
        return await (
            self._tofu()
                .with_exec([
                    "tofu",
                    "fmt",
                    "-check",
                    "-recursive",
                    "-write=false",
                    "-diff",
                ]).stdout()
        )

    async def validate(self) -> str:
        """Validate the code configuration"""
        return await (
            self._init()
                .with_exec([
                    "tofu",
                    "validate",
                ]).stdout()
        )

    def _init(self) -> dagger.Container:
        """Initialise OpenTofu layer"""

        return (
            self._tofu()
                .with_mounted_secret("/infra/credentials", self._tofu_context.credentials)
                .with_env_variable("GOOGLE_APPLICATION_CREDENTIALS", "/infra/credentials")
                .with_exec([
                    "tofu",
                    "init",
                    "-backend-config",
                    f"backend-configurations/{self._tofu_context.configuration}-backend.tfvars",
                ])
        )

    async def plan(self) -> str:
        """Generate an OpenTofu plan"""
        return await (
            self._init()
                .with_env_variable("CACHEBUSTER", str(datetime.now()))
                .with_exec([
                    "tofu",
                    "plan",
                    "-var-file",
                    f"./configurations/{self._tofu_context.configuration}.tfvars",
                    "-out",
                    f"/infra/plan/{self._tofu_context.configuration}.tofuplan",
                ]).stdout()
        )

    async def plan_destroy(self) -> str:
        """Generate an OpenTofu destroy plan"""
        return await (
            self._init()
                .with_env_variable("CACHEBUSTER", str(datetime.now()))
                .with_exec([
                    "tofu",
                    "plan",
                    "-destroy",
                    "-var-file",
                    f"./configurations/{self._tofu_context.configuration}.tfvars",
                    "-out",
                    f"/infra/plan/{self._tofu_context.configuration}.tofuplan",
                ]).stdout()
        )

    async def apply(self) -> str:
        """Apply all changes with a given plan"""
        return await (
            self._init()
                .with_env_variable("CACHEBUSTER", str(datetime.now()))
                .with_exec([
                    "tofu",
                    "apply",
                    f"/infra/plan/{self._tofu_context.configuration}.tofuplan",
                ]).stdout()
        )

    def _tofu(self) -> dagger.Container:
        """Return a configured container for OpenTofu"""

        return (
            dag.container()
            .from_(f"ghcr.io/opentofu/opentofu:{self._tofu_context.tofu_version}")
            .with_directory("/infra", self._tofu_context.directory)
            .with_mounted_cache(
                f"/infra/{self._tofu_context.layer}/.terraform",
                dag.cache_volume("terraform"),
                sharing=dagger.CacheSharingMode.SHARED
            )
            .with_mounted_cache(
                "/infra/plan",
                dag.cache_volume("plan"),
                sharing=dagger.CacheSharingMode.PRIVATE
            )
            .with_workdir(f"/infra/{self._tofu_context.layer}")
        )

    async def checkov(
        self,
        configuration: Annotated[dagger.File, DefaultPath(".checkov.yaml")],
    ) -> str:
        """Execute Checkov to run security analysis"""

        return await (
            dag.container()
            .from_(f"bridgecrew/checkov:{self._tofu_context.checkov_version}")
            .with_directory("/infra", self._tofu_context.directory)
            .with_file(f"/infra/{self._tofu_context.layer}/.checkov.yaml", configuration)
            .with_workdir(f"/infra/{self._tofu_context.layer}")
            .with_exec([
                "checkov",
                "-d",
                ".",
            ]).stdout()
        )

    async def tflint(
        self,
        configuration: Annotated[dagger.File, DefaultPath(".tflint.hcl")],
    ) -> str:
        """Execute Tflint to run best practices analysis"""

        return await (
            dag.container()
            .from_(f"ghcr.io/terraform-linters/tflint:{self._tofu_context.tflint_version}")
            .with_directory("/infra", self._tofu_context.directory)
            .with_file(f"/infra/{self._tofu_context.layer}/.tflint.hcl", configuration)
            .with_workdir(f"/infra/{self._tofu_context.layer}")
            .with_exec([
                "tflint",
                "--recursive",
            ]).stdout()
        )
