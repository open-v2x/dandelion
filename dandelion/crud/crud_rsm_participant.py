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

from typing import List, Optional, Tuple

from sqlalchemy import desc
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import Participants
from dandelion.schemas import RSMParticipantCreate, RSMParticipantUpdate
from dandelion.schemas.utils import Sort


class CRUDRSMParticipant(CRUDBase[Participants, RSMParticipantCreate, RSMParticipantUpdate]):
    """"""

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        sort: Sort = Sort.desc,
        ptc_type: Optional[str] = None,
    ) -> Tuple[int, List[Participants]]:
        query_ = db.query(self.model)
        if ptc_type is not None:
            query_ = query_.filter(self.model.ptc_type == ptc_type)
        total = query_.count()
        if sort == Sort.asc:
            query_ = query_.order_by(self.model.id)
        else:
            query_ = query_.order_by(desc(self.model.id))
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsm_participant = CRUDRSMParticipant(Participants)
