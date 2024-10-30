import dagger

class TofuContext:
    """The OpenTofu version"""
    @property
    def tofu_version(self) -> str:
        return self._tofu_version

    @tofu_version.setter
    def tofu_version(self, value: str = "latest"):
        self._tofu_version = value

    """Checkov version"""
    @property
    def checkov_version(self) -> str:
        return self._checkov_version

    @checkov_version.setter
    def checkov_version(self, value: str = "latest"):
        self._checkov_version = value

    """Tflint version"""
    @property
    def tflint_version(self) -> str:
        return self._tflint_version

    @tflint_version.setter
    def tflint_version(self, value: str = "latest"):
        self._tflint_version = value

    """The infrastructure directory to mount inside the OpenTofu container"""
    @property
    def directory(self) -> dagger.Directory:
        return self._directory

    @directory.setter
    def directory(self, value: dagger.Directory):
        self._directory = value

    """The selected folder to run OpenTofu commands"""
    @property
    def layer(self) -> str:
        return self._layer

    @layer.setter
    def layer(self, value: str = ""):
        self._layer = value

    """The Tfvars configuration file to create resources"""
    @property
    def configuration(self) -> str:
        return self._configuration

    @configuration.setter
    def configuration(self, value: str):
        self._configuration = value

    """The Cloud credentials to create resources"""
    @property
    def credentials(self) -> str:
        return self._credentials

    @credentials.setter
    def credentials(self, value: str):
        self._credentials = value

    def __init__(
		self,
		directory: dagger.Directory,
        layer: str,
		configuration: str,
		credentials: dagger.Secret, 
        tofu_version: str = "latest",
		checkov_version: str = "latest", 
        tflint_version: str = "latest"
	):

        """Initialize an OpenTofu context"""
        self._directory = directory
        self._layer = layer
        self._configuration = configuration
        self._credentials = credentials
        self._tofu_version = tofu_version
        self._checkov_version = checkov_version
        self._tflint_version = tflint_version
