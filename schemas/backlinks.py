from pydantic import BaseModel

class backlink_schema(BaseModel):
    link:str
    site:str
    status:str
    pa:str
    da:str
    last_check:str
