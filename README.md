# Dagger OpenTofu pipeline

This example uses [Dagger](https://dagger.io/), a programmable tool to run your CI/CD anywhere, with [OpenTofu](https://opentofu.org/) to deploy infrastructure as code in Google Cloud.

**Table of contents:**

* [Pipeline overview](#pipeline-overview)
* [Arguments](#arguments)
* [OpenTofu structure](#opentofu-structure)
* [Dagger code](#dagger-code)
  * [Cache invalidation](#cache-invalidation)
  * [Secrets handling](#secrets-handling)
* [Blog posts](#blog-posts)

## Pipeline overview

With this Dagger pipeline definition, you can do the following actions:

* Deploy resources with your code for a following folder (called *layer*) and configuration (.tfvars): ``dagger call deploy``;
* Destroy resources with your code for a following folder (called *layer*) and configuration (.tfvars): ``dagger call destroy``.

## Arguments

To call a Dagger Function, you have to define the following arguments:

* ``--directory``: Path to the folder containing your infrastructure as code;
* ``--layer``: Name of the folder you want to check, deploy or destroy;
* ``--configuration``: Name of the configuration (.tfvars) inside the folder define before you want to check, deploy or destroy;
* ``--credentials``: Path to the Google Cloud credentials file. For example: ``file:./google_application_credentials.json``;
* ``--tofu-version``: OpenTofu version to use (default: latest);
* ``--checkov-version``: Checkov version to use (default: latest);
* ``--tflint-version``: Tflint version to use (default: latest).

For example, to deploy the ``example`` configuration in the ``network`` folder, you can use:

```sh
dagger call deploy --directory=./infra --layer=network --configuration=example --credentials=file:./google_application_credentials.json
```

## OpenTofu structure

The OpenTofu source code is in the ``infra`` folder. Each sub-folder represents a **layer** of OpenTofu, except the ``modules`` folder containing common modules.

For a dedicated configuration, a ``.ftvars`` file needs to be created in the ``configurations`` folder and in the ``backend-configurations`` folder with a ``-backend`` suffix.

## Dagger code

The Dagger code is defined in the ``dagger`` folder, it uses the python SDK with source code in the ``src/main`` folder:

* ``__init__.py``: contains the entrypoint for Dagger;
* ``tofu_pipeline.py``: contains the implementation of the OpenTofu pipeline with Dagger Functions;
* ``tofu_context.py``: contains the definition context for OpenTofu for running the ``tofu`` commands;
* ``tofu_jobs.py``: contains the definition of the OpenTofu jobs such as fmt, validate, plan, destroy, etc.

### Cache invalidation

A cache invalidation is set in ``plan``, ``plan_destroy`` and ``apply`` functions in ``tofu_jobs.py`` file:

```python
.with_env_variable("CACHEBUSTER", str(datetime.now()))
```

This enforces OpenTofu to rerun each times these actions and avoid skipping these steps with the default Dagger cache as described in the [documentation](https://docs.dagger.io/cookbook/#invalidate-cache).

### Secrets handling

In the ``_init`` function used to perform the ``tofu init`` command, the file containing the service account for connecting to Google Cloud must be mounted within the container.

To do this, the [Dagger cookbook](https://docs.dagger.io/cookbook#mount-files-as-secrets) gives an example to be used with the *Dagger Function* ``with_mounted_secret``:

```python
def _init(self) -> dagger.Container:
    """Initialise OpenTofu layer"""

    return (
        self._tofu()
            .with_mounted_secret("/infra/credentials", self._tofu_context.credentials)
[...]
```

This method protects sensitive information without having to store it in hard coded format.

## Blog posts

Don't hesitate to read the following blog posts to find out more about Dagger with OpenTofu:

* [Dagger, the new CI/CD era?](https://blog.filador.fr/en/posts/dagger-the-new-ci-cd-era/) - English version
* [Dagger, la nouvelle ère de la CI/CD ?](https://blog.filador.fr/posts/dagger-la-nouvelle-ere-de-la-ci-cd/) - French version
