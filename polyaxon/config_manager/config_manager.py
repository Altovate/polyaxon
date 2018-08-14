import base64

from distutils.util import strtobool  # pylint:disable=import-error

from django.utils.functional import cached_property

from polyaxon_schemas.polyaxonfile import reader

from config_manager.exceptions import ConfigurationError
from config_manager.uri_spec import UriSpec


class ConfigManager(object):
    _PASS = '-Z$Swjin_bdNPtaV4nQEn&gWb;T|'

    def __init__(self, **params):
        self._params = params
        self._requested_keys = set()
        self._secret_keys = set()
        self._local_keys = set()
        self._testing_flag = self.get_boolean('TESTING', is_optional=True, default=False)
        self._env = self.get_string('POLYAXON_ENVIRONMENT')
        self._service = self.get_string('POLYAXON_SERVICE', is_local=True)
        self._is_debug_mode = self.get_boolean('POLYAXON_DEBUG', is_optional=True, default=False)
        self._namespace = self.get_string('POLYAXON_K8S_NAMESPACE')
        if self.is_sidecar_service or self.is_dockerizer_service:
            self._node_name = None
        else:
            self._node_name = self.get_string('POLYAXON_K8S_NODE_NAME', is_local=True)

    @property
    def namespace(self):
        return self._namespace

    @property
    def node_name(self):
        return self._node_name

    @property
    def service(self):
        return self._service

    @property
    def is_monolith_service(self):
        return self.service == 'monolith'

    @property
    def is_api_service(self):
        return self.service == 'api'

    @property
    def is_commands_service(self):
        return self.service == 'commands'

    @property
    def is_dockerizer_service(self):
        return self.service == 'dockerizer'

    @property
    def is_crons_service(self):
        return self.service == 'crons'

    @property
    def is_monitor_namespace_service(self):
        return self.service == 'monitor_namespace'

    @property
    def is_monitor_resources_service(self):
        return self.service == 'monitor_resources'

    @property
    def is_scheduler_service(self):
        return self.service == 'scheduler'

    @property
    def is_monitor_statuses_service(self):
        return self.service == 'monitor_statuses'

    @property
    def is_sidecar_service(self):
        return self.service == 'sidecar'

    @property
    def is_streams_service(self):
        return self.service == 'streams'

    @property
    def is_hpsearch_service(self):
        return self.service == 'hpsearch'

    @property
    def is_events_handlers_service(self):
        return self.service == 'events_handlers'

    @property
    def is_debug_mode(self):
        return self._is_debug_mode

    @property
    def env(self):
        return self._env

    @property
    def is_testing_env(self):
        if self._testing_flag:
            return True
        if self.env == 'testing':
            return True
        return False

    @property
    def is_local_env(self):
        if self.env == 'local':
            return True
        return False

    @property
    def is_staging_env(self):
        if self.env == 'staging':
            return True
        return False

    @property
    def is_production_env(self):
        if self.env == 'production':
            return True
        return False

    def setup_auditor_services(self):
        if not self.is_testing_env:
            import activitylogs
            import auditor
            import notifier
            import tracker

            auditor.validate()
            auditor.setup()
            tracker.validate()
            tracker.setup()
            activitylogs.validate()
            activitylogs.setup()
            notifier.validate()
            notifier.setup()

    def setup_publisher_service(self):
        import publisher

        publisher.validate()
        publisher.setup()

    def setup_query_service(self):
        import query

        query.validate()
        query.setup()

    def setup_stats_service(self):
        import stats

        stats.validate()
        stats.setup()

    @classmethod
    def read_configs(cls, config_values):  # pylint:disable=redefined-outer-name
        config = reader.read(config_values)  # pylint:disable=redefined-outer-name
        return cls(**config) if config else None

    @cached_property
    def decode_iterations(self):
        return self.get_int('_POLYAXON_DECODE_ITERATION', is_optional=True, default=1)

    @cached_property
    def notification_url(self):
        value = self.get_string(
            '_POLYAXON_NOTIFICATION',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None

    @cached_property
    def platform_dns(self):
        value = self.get_string(
            '_POLYAXON_PLATFORM_DNS',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None

    @cached_property
    def cli_dns(self):
        value = self.get_string(
            '_POLYAXON_CLI_DNS',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value, 2) if value else None

    @cached_property
    def tracker_key(self):
        value = self.get_string(
            '_POLYAXON_TRACKER_KEY',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None

    def params_startswith(self, term):
        return [k for k in self._params if k.startswith(term)]

    def params_endswith(self, term):
        return [k for k in self._params if k.endswith(term)]

    def get_requested_params(self, include_secrets=False, include_locals=False, to_str=False):
        params = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            if not include_locals and key in self._local_keys:
                continue
            value = self._params[key]
            params[key] = '{}'.format(value) if to_str else value
        return params

    def get_int(self,
                key,
                is_optional=False,
                is_secret=False,
                is_local=False,
                default=None,
                options=None):
        """Get a the value corresponding to the key and converts it to `int`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `int`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_float(self,
                  key,
                  is_optional=False,
                  is_secret=False,
                  is_local=False,
                  default=None,
                  options=None):
        """Get a the value corresponding to the key and converts it to `float`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `float`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=float,
                                     type_convert=float,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_boolean(self,
                    key,
                    is_optional=False,
                    is_secret=False,
                    is_local=False,
                    default=None,
                    options=None):
        """Get a the value corresponding to the key and converts it to `bool`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_string(self, key,
                   is_optional=False,
                   is_secret=False,
                   is_local=False,
                   default=None,
                   options=None):
        """Get a the value corresponding to the key and converts it to `str`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `str`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def _get(self, key):
        """Gets key from the dictionary made out of the configs passed.

        :param key: the dict key.
        :return: The corresponding value of the key if found.
        :raise: KeyError
        """
        return self._params[key]

    def _add_key(self, key, is_secret=False, is_local=False):
        self._requested_keys.add(key)
        if is_secret:
            self._secret_keys.add(key)
        if is_local:
            self._local_keys.add(key)

    @staticmethod
    def _check_options(key, value, options):
        if options and value not in options:
            raise ConfigurationError(
                'The value `{}` provided for key `{}` '
                'is not one of the possible values.'.format(value, key))

    def _get_typed_value(self,
                         key,
                         target_type,
                         type_convert,
                         is_optional=False,
                         is_secret=False,
                         is_local=False,
                         default=None,
                         options=None):
        """Returns the value corresponding to the key converted to the given type.

        :param key: the dict key.
        :param target_type: The type we expect the variable or key to be in.
        :param type_convert: A lambda expression that converts the key to the desired type.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.

        :return: The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise ConfigurationError(
                    'No value was provided for the non optional key `{}`.'.format(key))
            return default

        if isinstance(value, str):
            try:
                self._add_key(key, is_secret=is_secret, is_local=is_local)
                self._check_options(key=key, value=value, options=options)
                return type_convert(value)
            except ValueError:
                raise ConfigurationError("Cannot convert value `{}` (key: `{}`)"
                                         "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            self._add_key(key, is_secret=is_secret, is_local=is_local)
            self._check_options(key=key, value=value, options=options)
            return value
        raise ConfigurationError(key, value, target_type)

    def parse_uri_spec(self, uri_spec):
        parts = uri_spec.split('@')
        if len(parts) != 2:
            if self.is_debug_mode:
                raise ConfigurationError(
                    'Received invalid uri_spec `{}`. '
                    'It must be in the format `user:pass@host`'.format(uri_spec))
            else:
                return None

        user_pass, host = parts
        user_pass = user_pass.split(':')
        if len(user_pass) != 2:
            if self.is_debug_mode:
                raise ConfigurationError(
                    'Received invalid uri_spec `{}`. '
                    'It must be in the format `user:pass@host`'.format(uri_spec))
            else:
                return None

        return UriSpec(user=user_pass[0], password=user_pass[1], host=host)

    def _decode(self, value, iteration=3):
        iteration = iteration or self.decode_iterations

        def _decode_once():
            return base64.b64decode(value).decode('utf-8')

        for _ in range(iteration):
            value = _decode_once()
        return value

    @staticmethod
    def _encode(value):
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')