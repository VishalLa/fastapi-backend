from pydantic import BaseModel

# To enable ORM modle (allows to read SQLAlchemy objects)
class TunedModel(BaseModel):
    class Config:
        from_attributes = True