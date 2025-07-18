from pydantic import BaseModel, Field

class UsernameModel(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=32,
        pattern=r'^[А-Яа-яЁё]+$',
        description="Только кириллические буквы, от 1 до 32 символов"
    )