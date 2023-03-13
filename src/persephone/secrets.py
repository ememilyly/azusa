'''persephone.secrets

check for secrets in priority order:
    self._runtime_secrets   - allows for runtime setting of secrets for testing
    container               - /run/secrets
    env                     - environment
    <file>                  - config file from -s
'''

import os
import logging
from configparser import ConfigParser
from typing import Union

_log = logging.getLogger(__name__)


class Secrets():
    log = _log
    _runtime_secrets = {}
    secrets_file = None

    @classmethod
    def get(self, secret: str) -> Union[str, None]:
        if secret in self._runtime_secrets:
            return self._runtime_secrets[secret]
        elif os.path.isfile(f"/run/secrets/{secret.lower()}"):
            with open(f"/run/secrets/{secret.lower()}", "r") as f:
                return f.read()
        elif secret in os.environ:
            return os.environ[secret]
        elif self.secrets_file:
            if not os.path.isfile(self.secrets_file):
                raise FileNotFoundError(self.secrets_file)
            _config = ConfigParser()
            _config.read(self.secrets_file)
            return _config["persephone"][secret]
        else:
            return None

    @classmethod
    def set(self, secret: dict) -> None:
        self.log.warning(f"Setting runtime value for {', '.join(secret.keys())}")
        self._runtime_secrets = {**self._runtime_secrets, **secret}
