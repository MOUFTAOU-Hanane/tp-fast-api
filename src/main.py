from fastapi import FastAPI,Depends,HTTPException
from .schemas.schema import DictionnaryIn, DictionnaryOut,TraductionIn, TraductionOut,TraductionWordIn, TraductionWordOut
from sqlalchemy.orm import Session
from .repositories import repository
from .conf.database import SessionLocal
from .conf.database import Base, SessionLocal, engine
from typing import List

app = FastAPI()  
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
  
@app.post("/dictionaries/", response_model=DictionnaryOut)
def create_dictionnary(dictionnary: DictionnaryIn, db: Session = Depends(get_db)):
    db_dic = repository.get_dictionnary_by_name(db, name=dictionnary.name)
    if db_dic:
        raise HTTPException(status_code=400, detail="Cet nom existe déja dans la liste de votre dictionnaire")
    return repository.create_dictionnary(db=db, dictionnary=dictionnary)

@app.get("/dictionaries/{dictionnary_id}", response_model=DictionnaryOut)
def read_dictionnary(dictionnary_id: int, db: Session = Depends(get_db)):
    db_dic = repository.get_dictionary(db, dictionnary_id=dictionnary_id)
    if db_dic is None:
        raise HTTPException(status_code=404, detail="Ce dictionnaire n'existe pas dans la base")
    return db_dic

@app.get("/dictionaries/", response_model=list[DictionnaryOut])
def read_dictionnary(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dictionaries = repository.get_dictionaries(db, skip=skip, limit=limit)
    return dictionaries

@app.put("/dictionaries/{dictionnary_id}", response_model=DictionnaryOut)
def update_dictionnary(dictionnary_id: int, dictionnary: DictionnaryIn, db: Session = Depends(get_db)):
    db_dictionnary = repository.get_dictionary(db, dictionnary_id)
    if not db_dictionnary:
        raise HTTPException(status_code=404, detail="Ce dictionnaire n'existe pas dans la base")
    return repository.update_dictionnary(db=db, dictionnary_id=dictionnary_id, dictionnary=dictionnary)



@app.post("/traduction/", response_model=List[TraductionOut])
def create_traduction(traduction: TraductionIn, db: Session = Depends(get_db)):  
    return repository.create_traduction(db=db, traduction_create=traduction)


@app.get("/traductions/", response_model=List[TraductionOut])
def read_traductions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    traductions = repository.get_traductions(db, skip=skip, limit=limit)
    return traductions



@app.get("/traduction/{traduction_id}", response_model=list[TraductionOut])
def read_traduction(traduction_id: int, db: Session = Depends(get_db)):
    traduction = repository.get_traduction(db, traduction_id=traduction_id)
    return traduction

@app.post("/traduction_word/")
def traduction_word( traduction: TraductionWordIn, db: Session = Depends(get_db)):
        traduction_word = repository.traduction_word(db, traduction)
        return traduction_word

    
