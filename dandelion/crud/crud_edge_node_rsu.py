# Copyright 2022 99Cloud, Inc. All Rights Reserved.
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

from typing import List, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import EdgeNodeRSU
from dandelion.schemas import EdgeNodeRSUCreate, EdgeNodeRSUUpdate


class CRUDEdgeNodeRSU(CRUDBase[EdgeNodeRSU, EdgeNodeRSUCreate, EdgeNodeRSUUpdate]):
    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        node_id: int,
        area_code: str,
    ) -> Tuple[int, List[EdgeNodeRSU]]:
        query_ = db.query(self.model)
        if node_id is not None:
            query_ = query_.filter(self.model.edge_node_id == node_id)
        if area_code is not None:
            query_ = query_.filter(self.model.area_code == area_code)
        query_ = query_.filter(self.model.location != "{}")

        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data

    def get_by_node_id_esn(self, db: Session, *, edge_node_id: int, rsu_esn: str):
        return (
            db.query(self.model)
            .filter(self.model.edge_node_id == edge_node_id)
            .filter(self.model.esn == rsu_esn)
            .first()
        )

    def get_by_node_id_rsu(self, db: Session, *, edge_node_id: int, edge_rsu_id: int):
        return (
            db.query(self.model)
            .filter(self.model.edge_node_id == edge_node_id)
            .filter(self.model.edge_rsu_id == edge_rsu_id)
            .first()
        )

    def remove_by_node_id(self, db: Session, *, edge_node_id: int):
        db.execute(delete(self.model).where(self.model.edge_node_id == edge_node_id))
        db.commit()

    def remove_by_node_id_esn(self, db: Session, *, edge_node_id: int, rsu_esn: str):
        db.execute(
            delete(self.model).where(
                self.model.edge_node_id == edge_node_id, self.model.esn == rsu_esn
            )
        )
        db.commit()

    def create(self, db: Session, *, obj_in: EdgeNodeRSUCreate):
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


edge_node_rsu = CRUDEdgeNodeRSU(EdgeNodeRSU)
