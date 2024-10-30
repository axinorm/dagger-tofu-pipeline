import dagger

from dagger import Doc, DefaultPath, function, object_type
from typing import Annotated

from .tofu_context import TofuContext
from .tofu_jobs import TofuJobs

@object_type
class TofuPipeline:
    @function
    async def deploy(
        self,
        directory: Annotated[dagger.Directory, Doc("OpenTofu source directory")],
        layer: Annotated[str, Doc("Infrastructure layer")],
        configuration: Annotated[str, Doc("Configuration to run")],
        credentials: Annotated[dagger.Secret, Doc("Google Cloud credentials")],
        checkov_configuration: Annotated[dagger.File, DefaultPath(".checkov.yaml")],
        tflint_configuration: Annotated[dagger.File, DefaultPath(".tflint.hcl")],
        tofu_version: Annotated[str, Doc("OpenTofu version")] = "latest",
        checkov_version: Annotated[str, Doc("Checkov version")] = "latest",
        tflint_version: Annotated[str, Doc("Tflint version")] = "latest",
    ):
        """Run the OpenTofu deploy pipeline"""

        tofu_context = TofuContext(
            directory=directory,
            layer=layer,
            configuration=configuration,
            credentials=credentials,
            tofu_version=tofu_version,
            checkov_version=checkov_version,
            tflint_version=tflint_version
        )
        
        tofu_jobs = TofuJobs(tofu_context)

        await tofu_jobs.format()
        await tofu_jobs.validate()
        await tofu_jobs.tflint(tflint_configuration)
        await tofu_jobs.checkov(checkov_configuration)
        await tofu_jobs.plan()
        await tofu_jobs.apply()

    @function
    async def destroy(
        self,
        directory: Annotated[dagger.Directory, Doc("OpenTofu source directory")],
        layer: Annotated[str, Doc("Infrastructure layer")],
        configuration: Annotated[str, Doc("Configuration to run")],
        credentials: Annotated[dagger.Secret, Doc("Google Cloud credentials")],
        checkov_configuration: Annotated[dagger.File, DefaultPath(".checkov.yaml")],
        tflint_configuration: Annotated[dagger.File, DefaultPath(".tflint.hcl")],
        tofu_version: Annotated[str, Doc("OpenTofu version")] = "latest",
        checkov_version: Annotated[str, Doc("Checkov version")] = "latest",
        tflint_version: Annotated[str, Doc("Tflint version")] = "latest",
    ):
        """Run the OpenTofu destroy pipeline"""

        tofu_context = TofuContext(
            directory=directory,
            layer=layer,
            configuration=configuration,
            credentials=credentials,
            tofu_version=tofu_version,
            checkov_version=checkov_version,
            tflint_version=tflint_version
        )
        
        tofu_jobs = TofuJobs(tofu_context)

        await tofu_jobs.format()
        await tofu_jobs.validate()
        await tofu_jobs.tflint(tflint_configuration)
        await tofu_jobs.checkov(checkov_configuration)
        await tofu_jobs.plan_destroy()
        await tofu_jobs.apply()
