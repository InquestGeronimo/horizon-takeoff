from typing import List, Optional
from pydantic import BaseModel


class EC2Config(BaseModel):
    region_name: str
    ami_id: str
    instance_type: str
    key_name: str
    security_group_ids: List[str]
    instance_ids: Optional[List[str]] = None
