from typing import Any

from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
    slug:str; name:str; timezone:str="Europe/Vienna"; default_language:str="de-AT"
    phone:str|None=None; address:str|None=None
    reservation_provider:str="mock"; reservation_config:dict[str,Any]={}
    pos_provider:str="none"; pos_config:dict[str,Any]={}

class KnowledgeIn(BaseModel):
    kind:str="general"; title:str=""; content:str=Field(min_length=2); metadata:dict[str,Any]={}

class ChatIn(BaseModel):
    message:str=Field(min_length=1,max_length=4000); user_id:str="web-anonymous"; session_id:str|None=None
