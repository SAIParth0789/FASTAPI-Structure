from pydantic import BaseModel, ConfigDict, validator
from typing import List, Optional

class User(BaseModel):
    email: str


class AdminUserIn(User):
    model_config = ConfigDict(from_attributes=True)
    password: str