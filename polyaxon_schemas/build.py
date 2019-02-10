# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.utils import BuildBackend


def validate_image(image):
    if not image:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    tagged_image = image.split(':')
    if len(tagged_image) > 3:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    if len(tagged_image) == 3 and ('/' not in tagged_image[1] or tagged_image[1].startswith('/')):
        raise ValidationError('Invalid docker image `{}`'.format(image))


def validate_backend(backend):
    if backend and backend not in BuildBackend.VALUES:
        raise ValidationError('Build backend `{}` not supported'.format(backend))


class BuildSchema(BaseSchema):
    backend = fields.Str(allow_none=True)
    image = fields.Str()
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    ref = fields.Str(allow_none=True)
    nocache = fields.Boolean(allow_none=True)

    @staticmethod
    def schema_config():
        return BuildConfig

    @validates_schema
    def validate_image(self, data):
        """Validates docker image structure"""
        validate_image(data.get('image'))

    @validates_schema
    def validate_backend(self, data):
        """Validate backend"""
        validate_backend(data.get('backend'))


class BuildConfig(BaseConfig):
    """
    Build config.

    Args:
        image: str. The name of the image to use during the build step.
        build_steps: list(str). The build steps to apply to your docker image.
            (translate to multiple RUN ...)
        env_vars: list((str, str)) The environment variable to set on you docker image.
        nocache: `bool`. To not use cache when building the image.
        ref: `str`. The commit/branch/treeish to use.

    """
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = ['build_steps', 'env_vars', 'nocache', 'ref', 'backend']

    def __init__(self,
                 image,
                 backend=None,
                 build_steps=None,
                 env_vars=None,
                 nocache=None,
                 ref=None):
        validate_image(image)
        validate_backend(backend)
        self.backend = backend
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.nocache = nocache
        self.ref = ref

    @property
    def image_tag(self):
        tagged_image = self.image.split(':')
        if len(tagged_image) == 1:
            return 'latest'
        if len(tagged_image) == 2:
            return 'latest' if '/' in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
