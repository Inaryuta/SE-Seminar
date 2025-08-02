from pydantic import BaseModel

class ExerciseBase(BaseModel):
    name: str
    type: str

class ExerciseCreate(ExerciseBase):
    pass  

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        orm_mode = True
