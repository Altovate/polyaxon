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

from marshmallow import ValidationError

from coredb.abstracts.runs import BaseRun
from polyaxon.exceptions import PolyaxonCompilerError, PolyaxonSchemaError
from polyaxon.polyaxonfile import CompiledOperationSpecification
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler import resolver
from polyaxon.polypod.compiler.resolvers import CoreResolver
from polycommon.exceptions import AccessNotAuthorized, AccessNotFound


class CorePlatformResolver(CoreResolver):
    def resolve_params(self):
        params = self.run.params or {}
        self.compiled_operation = CompiledOperationSpecification.apply_params(
            config=self.compiled_operation, params=params, context=self.globals,
        )

    def resolve_io(self):
        self.run.content = self.compiled_operation.to_dict(
            dump=True
        )  # TODO: check if this needed or not
        if self.compiled_operation.inputs:
            self.run.inputs = {
                io.name: io.value for io in self.compiled_operation.inputs
            }
        if self.compiled_operation.outputs:
            self.run.outputs = {
                io.name: io.value for io in self.compiled_operation.outputs
            }

    def resolve_state(self):
        self.run.save(update_fields=["content", "inputs", "outputs", "meta_info"])


def resolve(run: BaseRun, resolver_cls=None):
    resolver_cls = resolver_cls or CorePlatformResolver
    try:
        project = run.project
        return resolver.resolve(
            run=run,
            compiled_operation=V1CompiledOperation.read(run.content),
            owner_name=project.owner.name,
            project_name=project.name,
            project_uuid=project.uuid.hex,
            run_uuid=run.uuid.hex,
            run_name=run.name,
            run_path=run.subpath,
            resolver_cls=resolver_cls,
            params=None,
        )
    except (
        AccessNotAuthorized,
        AccessNotFound,
        ValidationError,
        PolyaxonSchemaError,
    ) as e:
        raise PolyaxonCompilerError("Compilation Error: %s" % e) from e
