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

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSUQueryResultData
from dandelion.schemas import RSUQueryResultDataCreate


class CRUDRSUQueryResultData(
    CRUDBase[RSUQueryResultData, RSUQueryResultDataCreate, RSUQueryResultDataCreate]
):
    """"""

    def create_result_data(
        self, db: Session, *, obj_in: RSUQueryResultDataCreate
    ) -> RSUQueryResultData:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_by_result_id(self, db: Session, *, result_id: int):
        db.query(self.model).filter(self.model.result_id == result_id).delete()


rsu_query_result_data = CRUDRSUQueryResultData(RSUQueryResultData)
