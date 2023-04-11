# Copyright 2023 99Cloud, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase


class ServiceType(Base, DandelionBase):
    __tablename__ = "service_type"

    name = Column(String(64), nullable=False, unique=True)
    description = Column(Text)

    services = relationship("Service", backref="service_type")

    def __repr__(self) -> str:
        return (
            f"<service_type(id='{self.id}', name='{self.name}', "
            f"description='{self.description}')>"
        )

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                name=self.name,
                description=self.description,
            ),
        }


class Service(Base, DandelionBase):
    __tablename__ = "service"

    name = Column(String(64), nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("service_type.id"))
    vendor = Column(String(64))
    description = Column(Text)

    endpoints = relationship("Endpoint", backref="service")

    def __repr__(self) -> str:
        return (
            f"<service(id='{self.id}', name='{self.name}', "
            f"type_id='{self.type_id}', vendor='{self.vendor}', "
            f"description='{self.description}')>"
        )

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                name=self.name,
                type_id=self.type_id,
                vendor=self.vendor,
                description=self.description,
            ),
        }


class Endpoint(Base, DandelionBase):
    __tablename__ = "endpoint"

    name = Column(String(64), nullable=False, unique=True)
    service_id = Column(Integer, ForeignKey("service.id"))
    version = Column(String(64))
    url = Column(String(256), nullable=False)

    matadatas = relationship("EndpointMetadata", backref="endpoint")

    def __repr__(self) -> str:
        return (
            f"<endpoint(id='{self.id}', name='{self.name}', "
            f"service_id='{self.service_id}', version='{self.version}, "
            f"url='{self.url}')>"
        )

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                name=self.name,
                service_id=self.service_id,
                version=self.version,
                url=self.url,
            ),
        }


class EndpointMetadata(Base, DandelionBase):
    __tablename__ = "endpoint_metadata"

    endpoint_id = Column(Integer, ForeignKey("endpoint.id"))
    key = Column(String(64), nullable=False)
    value = Column(String(256))

    UniqueConstraint(endpoint_id, key, name="idx_endpoint_key")

    def __repr__(self) -> str:
        return (
            f"<endpoint(id='{self.id}', endpoint_id='{self.endpoint_id}', "
            f"key='{self.key}, value='{self.value}')>"
        )

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                endpoint_id=self.endpoint_id,
                key=self.key,
                value=self.value,
            ),
        }
