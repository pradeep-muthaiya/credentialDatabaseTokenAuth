from pydantic import BaseModel, Field

class UserNamePassword(BaseModel):
    username: str = Field(description="Username of client")
    password: str = Field(description="Password of client")