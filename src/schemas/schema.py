from pydantic import BaseModel
from typing import List

# Definiation de l'objet de l'utilisateur pour la validation
class DictionnaryIn(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

class DictionnaryOut(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        
class LineBase(BaseModel):
    key: str
    value: str
    
class TraductionIn(BaseModel):
    dictionnary_id: int
    lines: List[LineBase]
    class Config:
        orm_mode = True

class TraductionOut(BaseModel):
    id: int
    key: str
    value: str
    dictionnary_id: int
    class Config:
        orm_mode = True
    

class TraductionWordIn(BaseModel):
    word: str
    dictionnary_id: int
    class Config:
        orm_mode = True
    
class TraductionWordOut(BaseModel):
    word: str
    dictionnary_id: int
    traduction:str
    class Config:
        orm_mode = True
        
class TraductionnaryIn(BaseModel):
    name: str
    lines: List[LineBase]
    class Config:
        orm_mode = True
        
class TraductionaryOut(BaseModel):
    name: str
    lines: List[LineBase]
    class Config:
        orm_mode = True
        
class LineUpdate(BaseModel):
    id: int
    key: str
    value: str

class TraductionaryUpdate(BaseModel):
    dictionnary_id: int
    name: str 
    lines: List[LineUpdate]
        

    
    
