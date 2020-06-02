#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.deploy.schemas.auth import AuthSchema
from polyaxon.deploy.schemas.deployment_types import DeploymentCharts, DeploymentTypes
from polyaxon.deploy.schemas.email import EmailSchema
from polyaxon.deploy.schemas.ingress import IngressSchema
from polyaxon.deploy.schemas.intervals import IntervalsSchema
from polyaxon.deploy.schemas.rbac import RBACSchema
from polyaxon.deploy.schemas.root_user import RootUserSchema
from polyaxon.deploy.schemas.security_context import SecurityContextSchema
from polyaxon.deploy.schemas.service import (
    AgentServiceSchema,
    ApiServiceSchema,
    ExternalServicesSchema,
    HelperServiceSchema,
    HooksSchema,
    PostgresqlSchema,
    RabbitmqSchema,
    RedisSchema,
    ServiceSchema,
    WorkerServiceSchema,
)
from polyaxon.deploy.schemas.service_types import ServiceTypes
from polyaxon.deploy.schemas.ssl import SSLSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.types import ConnectionTypeSchema


def check_postgres(postgresql, external_services):
    postgresql_disabled = postgresql.enabled is False if postgresql else False
    external_postgresql = None
    if external_services:
        external_postgresql = external_services.postgresql

    if postgresql_disabled and not external_postgresql:
        raise ValidationError(
            "A postgresql instance is required, "
            "please enable the in-cluster postgresql, "
            "or provide an external instance."
        )


def check_rabbitmq(rabbitmq, external_services, broker):
    rabbitmq_enabled = rabbitmq and rabbitmq.enabled
    external_rabbitmq = None
    rabbitmq_borker = broker != "redis"
    if external_services:
        external_rabbitmq = external_services.rabbitmq

    if rabbitmq_enabled and external_rabbitmq:
        raise ValidationError(
            "You can either enable the in-cluster rabbitmq or use an external instance, "
            "not both!"
        )
    rabbitmq_used = rabbitmq_enabled or external_rabbitmq
    if rabbitmq_used and not rabbitmq_borker:
        raise ValidationError(
            "rabbitmq is enabled but you are using a different broker backend!"
        )

    return rabbitmq_used


def check_redis(redis, external_services, broker):
    redis_enabled = redis and redis.enabled
    external_redis = None
    redis_borker = broker == "redis"
    if external_services:
        external_redis = external_services.redis

    if redis_enabled and external_redis:
        raise ValidationError(
            "You can either enable the in-cluster redis or use an external instance, "
            "not both!"
        )

    redis_used = redis_enabled or external_redis
    if redis_used and not redis_borker:
        raise ValidationError(
            "redis is enabled but you are using a different broker backend!"
        )

    return redis_used


def broker_is_required(services):
    for s in services:
        if s and s.enabled:
            return True
    return False


def wrong_agent_deployment_keys(**kwargs):
    error_keys = []
    for k, v in kwargs.items():
        if v is not None:
            error_keys.append(k)
    if error_keys:
        raise ValidationError(
            "Agent deployment received some keys that are not required.\n"
            "Please remove these config keys from your config file:\n"
            "{}".format(error_keys)
        )


def validate_platform_deployment(
    postgresql, redis, rabbitmq, broker, scheduler, worker, beat, external_services
):
    check_postgres(postgresql, external_services)
    redis_used = check_redis(redis, external_services, broker)
    rabbitmq_used = check_rabbitmq(rabbitmq, external_services, broker)
    if rabbitmq_used and redis_used:
        raise ValidationError(
            "You can only enable rabbitmq or redis, you don't need to deploy both!"
        )
    broker_defined = rabbitmq_used or redis_used
    services = [scheduler, worker, beat]
    if broker_is_required(services) and not broker_defined:
        raise ValidationError(
            "You enabled some services that require a broker, please set redis or rabbitmq!"
        )


def validate_deployment_chart(
    deployment_chart, agent, environment,
):
    if deployment_chart == DeploymentCharts.AGENT and not agent:
        raise ValidationError(
            "Agent deployment requires a valid `agent` key configuration."
        )

    if (
        deployment_chart == DeploymentCharts.PLATFORM
        and agent
        and environment != "staging"
    ):
        raise ValidationError("Platform deployment received an unexpected `agent` key.")


def validate_gateway(gateway):
    if not gateway or not gateway.service:
        return
    service_type = gateway.service.get("type")
    if service_type and service_type not in ServiceTypes.VALUES:
        raise ValidationError(
            "Receive an invalid gateway service type: {}".format(service_type)
        )


class DeploymentSchema(BaseCamelSchema):
    deployment_type = fields.Str(
        allow_none=True, validate=validate.OneOf(DeploymentTypes.VALUES)
    )
    deployment_chart = fields.Str(
        allow_none=True,
        validate=validate.OneOf(DeploymentCharts.VALUES),
        default=DeploymentCharts.PLATFORM,
    )
    deployment_version = fields.Str(allow_none=True)
    namespace = fields.Str(allow_none=True)
    rbac = fields.Nested(RBACSchema, allow_none=True)
    polyaxon_secret = fields.Str(allow_none=True)
    internal_token = fields.Str(allow_none=True)
    password_length = fields.Int(allow_none=True)
    ssl = fields.Nested(SSLSchema, allow_none=True)
    encryption_secret = fields.Str(allow_none=True)
    admin_view_enabled = fields.Bool(allow_none=True)
    timezone = fields.Str(allow_none=True)
    environment = fields.Str(allow_none=True)
    ingress = fields.Nested(IngressSchema, allow_none=True)
    user = fields.Nested(RootUserSchema, allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(allow_none=True), allow_none=True)
    affinity = fields.Dict(allow_none=True)
    limit_resources = fields.Bool(allow_none=True)
    global_replicas = fields.Int(allow_none=True)
    global_concurrency = fields.Int(allow_none=True)
    gateway = fields.Nested(ApiServiceSchema, allow_none=True)
    api = fields.Nested(ApiServiceSchema, allow_none=True)
    streams = fields.Nested(ApiServiceSchema, allow_none=True)
    scheduler = fields.Nested(WorkerServiceSchema, allow_none=True)
    worker = fields.Nested(WorkerServiceSchema, allow_none=True)
    beat = fields.Nested(ServiceSchema, allow_none=True)
    agent = fields.Nested(AgentServiceSchema, allow_none=True)
    operator = fields.Nested(ServiceSchema, allow_none=True)
    init = fields.Nested(HelperServiceSchema, allow_none=True)
    sidecar = fields.Nested(HelperServiceSchema, allow_none=True)
    tables_hook = fields.Nested(ServiceSchema, allow_none=True)
    hooks = fields.Nested(HooksSchema, allow_none=True)
    postgresql = fields.Nested(PostgresqlSchema, allow_none=True)
    redis = fields.Nested(RedisSchema, allow_none=True)
    rabbitmq = fields.Nested(RabbitmqSchema, data_key="rabbitmq-ha", allow_none=True)
    broker = fields.Str(allow_none=True, validate=validate.OneOf(["redis", "rabbitmq"]))
    email = fields.Nested(EmailSchema, allow_none=True)
    ldap = fields.Raw(allow_none=True)
    metrics = fields.Raw(allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    host_name = fields.Str(allow_none=True)
    allowed_hosts = fields.List(fields.Str(), allow_none=True)
    intervals = fields.Nested(IntervalsSchema, allow_none=True)
    artifacts_store = fields.Nested(ConnectionTypeSchema, allow_none=True)
    connections = fields.List(fields.Nested(ConnectionTypeSchema), allow_none=True)
    notification_connections = fields.List(
        fields.Nested(ConnectionTypeSchema), allow_none=True,
    )
    log_level = fields.Str(allow_none=True)
    tracker_backend = fields.Str(allow_none=True)
    security_context = fields.Nested(SecurityContextSchema, allow_none=True)
    external_services = fields.Nested(ExternalServicesSchema, allow_none=True)
    debug_mode = fields.Bool(allow_none=True)
    organization_key = fields.Str(allow_none=True)
    auth = fields.Nested(AuthSchema, allow_none=True)

    # Pending validation
    dns = fields.Raw(allow_none=True)

    @staticmethod
    def schema_config():
        return DeploymentConfig

    @validates_schema
    def validate_deployment(self, data, **kwargs):
        validate_deployment_chart(
            deployment_chart=data.get("deployment_chart"),
            agent=data.get("agent"),
            environment=data.get("environment"),
        )
        validate_platform_deployment(
            postgresql=data.get("postgresql"),
            redis=data.get("redis"),
            rabbitmq=data.get("rabbitmq"),
            broker=data.get("broker"),
            scheduler=data.get("scheduler"),
            worker=data.get("worker"),
            beat=data.get("beat"),
            external_services=data.get("external_services"),
        )
        validate_gateway(data.get("gateway"))
        if data.get("deployment_chart") == DeploymentCharts.AGENT:
            wrong_agent_deployment_keys(
                polyaxon_secret=data.get("polyaxon_secret"),
                internal_token=data.get("internal_token"),
                password_length=data.get("password_length"),
                admin_view_enabled=data.get("admin_view_enabled"),
                user=data.get("user"),
                global_replicas=data.get("global_replicas"),
                global_concurrency=data.get("global_concurrency"),
                api=data.get("api"),
                scheduler=data.get("scheduler"),
                worker=data.get("worker"),
                beat=data.get("beat"),
                tables_hook=data.get("tables_hook"),
                hooks=data.get("hooks"),
                postgresql=data.get("postgresql"),
                redis=data.get("redis"),
                rabbitmq=data.get("rabbitmq"),
                broker=data.get("broker"),
                email=data.get("email"),
                ldap=data.get("ldap"),
                intervals=data.get("intervals"),
                metrics=data.get("metrics"),
                organization_key=data.get("organization_key"),
            )


class DeploymentConfig(BaseConfig):
    SCHEMA = DeploymentSchema

    def __init__(
        self,
        deployment_type=None,
        deployment_chart=None,
        deployment_version=None,
        namespace=None,
        rbac=None,
        polyaxon_secret=None,
        internal_token=None,
        password_length=None,
        ssl=None,
        encryption_secret=None,
        admin_view_enabled=None,
        timezone=None,
        environment=None,
        ingress=None,
        user=None,
        node_selector=None,
        tolerations=None,
        affinity=None,
        limit_resources=None,
        global_replicas=None,
        global_concurrency=None,
        gateway=None,
        api=None,
        streams=None,
        scheduler=None,
        worker=None,
        beat=None,
        agent=None,
        operator=None,
        init=None,
        sidecar=None,
        tables_hook=None,
        hooks=None,
        postgresql=None,
        redis=None,
        rabbitmq=None,
        broker=None,
        email=None,
        ldap=None,
        metrics=None,
        image_pull_secrets=None,
        host_name=None,
        allowed_hosts=None,
        intervals=None,
        artifacts_store=None,
        connections=None,
        notification_connections=None,
        log_level=None,
        tracker_backend=None,
        security_context=None,
        external_services=None,
        debug_mode=None,
        auth=None,
        organization_key=None,
        dns=None,
    ):
        validate_deployment_chart(
            deployment_chart=deployment_chart, agent=agent, environment=environment,
        )
        validate_platform_deployment(
            postgresql=postgresql,
            redis=redis,
            rabbitmq=rabbitmq,
            broker=broker,
            scheduler=scheduler,
            worker=worker,
            beat=beat,
            external_services=external_services,
        )
        validate_gateway(gateway)
        self.deployment_type = deployment_type
        self.deployment_chart = deployment_chart
        self.deployment_version = deployment_version
        self.namespace = namespace
        self.rbac = rbac
        self.polyaxon_secret = polyaxon_secret
        self.internal_token = internal_token
        self.password_length = password_length
        self.ssl = ssl
        self.dns = dns
        self.encryption_secret = encryption_secret
        self.admin_view_enabled = admin_view_enabled
        self.timezone = timezone
        self.environment = environment
        self.ingress = ingress
        self.user = user
        self.node_selector = node_selector
        self.tolerations = tolerations
        self.affinity = affinity
        self.limit_resources = limit_resources
        self.global_replicas = global_replicas
        self.global_concurrency = global_concurrency
        self.gateway = gateway
        self.api = api
        self.streams = streams
        self.scheduler = scheduler
        self.worker = worker
        self.beat = beat
        self.agent = agent
        self.operator = operator
        self.init = init
        self.sidecar = sidecar
        self.tables_hook = tables_hook
        self.hooks = hooks
        self.postgresql = postgresql
        self.redis = redis
        self.rabbitmq = rabbitmq
        self.broker = broker
        self.email = email
        self.ldap = ldap
        self.metrics = metrics
        self.image_pull_secrets = image_pull_secrets
        self.host_name = host_name
        self.allowed_hosts = allowed_hosts
        self.intervals = intervals
        self.artifacts_store = artifacts_store
        self.connections = connections
        self.notification_connections = notification_connections
        self.log_level = log_level
        self.tracker_backend = tracker_backend
        self.security_context = security_context
        self.external_services = external_services
        self.debug_mode = debug_mode
        self.auth = auth
        self.organization_key = organization_key
        if self.deployment_chart == DeploymentCharts.AGENT:
            wrong_agent_deployment_keys(
                polyaxon_secret=polyaxon_secret,
                internal_token=internal_token,
                password_length=password_length,
                admin_view_enabled=admin_view_enabled,
                user=user,
                global_replicas=global_replicas,
                global_concurrency=global_concurrency,
                api=api,
                scheduler=scheduler,
                worker=worker,
                beat=beat,
                tables_hook=tables_hook,
                hooks=hooks,
                postgresql=postgresql,
                redis=redis,
                rabbitmq=rabbitmq,
                broker=broker,
                email=email,
                ldap=ldap,
                intervals=intervals,
                metrics=metrics,
                organization_key=organization_key,
            )
