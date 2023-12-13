from sqlalchemy.orm import Session
from ..import models, schemas
from ..models.Dictionnary import Dictionnary
from ..models.Traduction import Traduction
from ..schemas.schema import DictionnaryIn, DictionnaryOut, TraductionIn, TraductionWordIn,TraductionnaryIn, TraductionaryOut, TraductionaryUpdate, LineBase
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional




#CRUUD DICTIONNARY
def get_dictionary(db: Session, dictionnary_id: int) -> Optional[dict]:
    dictionnary = db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()

    if not dictionnary:
        # Retourner None si le dictionnaire n'est pas trouvé
        return None

    traductions = db.query(Traduction).filter(Traduction.dictionnary_id == dictionnary_id).all()

    # Construire la réponse avec le dictionnaire et ses traductions
    response_data = {
        "dictionnary_name":dictionnary.name,
        "traductions": [
            {
                "id": traduction.id,
                "key": traduction.key,
                "value": traduction.value
            }
            for traduction in traductions
        ]
    }

    return response_data


def get_dictionaries(db: Session) -> Optional[List[dict]]:
    try:
        dictionaries = db.query(Dictionnary).all()

        if not dictionaries:
            return None  # Aucun dictionnaire trouvé dans la base de données

        result = []
        for dictionnary in dictionaries:
            traductions = db.query(Traduction).filter(Traduction.dictionnary_id == dictionnary.id).all()

            dictionnary_data = {
                "dictionnary": {
                    "id": dictionnary.id,
                    "name": dictionnary.name,
                },
                "traductions": [
                    {
                        "id": traduction.id,
                        "key": traduction.key,
                        "value": traduction.value
                    }
                    for traduction in traductions
                ]
            }

            result.append(dictionnary_data)

        return result

    except Exception as e:
        # Gérer les erreurs appropriées, par exemple, les exceptions de base de données
        print(f"Erreur lors de la récupération des dictionnaires : {str(e)}")
        return None


def get_dictionnary_by_name(db: Session, name: str):
    return db.query(Dictionnary).filter(Dictionnary.name == name).first()
    


# def get_dictionaries(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Dictionnary).offset(skip).limit(limit).all()


def create_dictionnary(db: Session, dictionnary: DictionnaryIn):
    db_dictionnary = Dictionnary(**dictionnary.dict())
    db.add(db_dictionnary)
    db.commit()
    db.refresh(db_dictionnary)
    return db_dictionnary

def update_dictionnary(db: Session, dictionnary: DictionnaryIn, dictionnary_id: int):
    dictionnary_in_db = db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()
    dictionnary_in_db.name = dictionnary.name
    db.commit()
    db.refresh(dictionnary_in_db)
    return dictionnary_in_db



#CRUD TRADUCTION
def get_traduction(db: Session, traduction_id: int):
    return db.query(Traduction).filter(Traduction.id == traduction_id).first()

def get_traductions(db: Session, skip: int = 0, limit: int = 300):
    return db.query(Traduction).offset(skip).limit(limit).all()

def create_traduction(db: Session, traduction_create: TraductionIn):
    traductions = []

    for line_create in traduction_create.lines:
        traduction = Traduction(
            key=line_create.key,
            value=line_create.value,
            dictionnary_id=traduction_create.dictionnary_id
        )

        db.add(traduction)
        traductions.append(traduction)

    db.commit()
    return traductions 

def update_traduction(db: Session, traduction: TraductionIn, traduction_id: int):
    traduction_in_db = db.query(Traduction).filter(Traduction.id == traduction_id).first()

    traduction_in_db.dictionnary_id = traduction.dictionnary_id

    db.query(Line).filter(Line.translation_id == traduction_id).delete()

    for line_create in traduction.lines:
        line = Line(key=line_create.key, value=line_create.value)
        traduction_in_db.lines.append(line)
        db.add(line)

    db.commit()

    db.refresh(traduction_in_db)

    return traduction_in_db

#CRUD COMBINAISON TRADUCTION & DICTIONNARY
def create_traduction_and_get_result(db: Session, traduction_create: TraductionnaryIn):
    try:
            db_dictionnary = db.query(Dictionnary).filter(Dictionnary.name == traduction_create.name).first()
            if db_dictionnary:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le dictionnaire existe déjà dans la base de données."
                )

            db_dictionnary = Dictionnary(name=traduction_create.name)
            db.add(db_dictionnary)
            db.commit()

            # Créer les données de traduction
            traduction_data = [
                {
                    "key": line_create.key,
                    "value": line_create.value,
                    "dictionnary_id": db_dictionnary.id,
                }
                for line_create in traduction_create.lines
            ]

            existing_keys = db.query(Traduction.key).filter(
                Traduction.key.in_([line_create.key for line_create in traduction_create.lines]),
                Traduction.dictionnary_id == db_dictionnary.id
            ).all()

            if existing_keys:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Les mots {existing_keys} ont déjà une traduction dans ce dictionnaire."
                )
            db.execute(Traduction.__table__.insert().values(traduction_data))
            db.commit()
            traductions = db.query(Traduction).filter(Traduction.dictionnary_id == db_dictionnary.id).all()
             # Inclure les ID dans la réponse
            traductions_with_id = [
            {
                "id": traduction.id,
                "key": traduction.key,
                "value": traduction.value
            }
            for traduction in traductions
        ]
            
            return {
            "dictionnary_id": db_dictionnary.id,
            "dictionnary_name": db_dictionnary.name,
            "traduction": traductions_with_id
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


def update_traduction(db: Session, traduction_update: TraductionaryUpdate):
    db_dictionnary = db.query(Dictionnary).filter(Dictionnary.id == traduction_update.dictionnary_id).first()

    if db_dictionnary:
        # Mettre à jour le nom du dictionnaire si nécessaire
        if traduction_update.name:
            db_dictionnary.name = traduction_update.name
            db.commit()

        # Mettre à jour les traductions
        for line_update in traduction_update.lines:
            db.query(Traduction).filter(
                Traduction.id == line_update.id
            ).update(
                {"key": line_update.key,"value": line_update.value},
                synchronize_session=False
            )

        db.commit()

        # Récupérer le dictionnaire mis à jour avec ses traductions
        db.refresh(db_dictionnary)
        
        result = TraductionaryOut(
            name=db_dictionnary.name,
            lines=[
                LineBase(key=line.key, value=line.value)
                for line in traduction_update.lines
            ]
        )

        return {"result": result}

    return {"error": "Dictionnaire non trouvé"}

def delete_dictionary(db: Session, dictionary_id: int) -> bool:
    try:
        dictionary = db.query(Dictionnary).filter(Dictionnary.id == dictionary_id).first()

        if not dictionary:
            return False  

        db.query(Traduction).filter(Traduction.dictionnary_id == dictionary_id).delete()

        db.delete(dictionary)
        db.commit()

        return {
            "success" :True,
            "message":"Le dictionnnaire a bien été supprimé"
        }  

    except Exception as e:
        print(f"Error deleting dictionary: {str(e)}")
        db.rollback()
        return False

def traduction_word(db: Session, traduction):
    try:
        array_trad = []
        word = traduction.word.upper()
        dictionnary_name = db.query(Dictionnary).filter(Dictionnary.id ==  traduction.dictionnary_id).first()
        for item in word:
            translation = db.query(Traduction).filter(Traduction.key == item, Traduction.dictionnary_id == traduction.dictionnary_id).first()
            if translation:
                array_trad.append(translation.value)
            else:
                array_trad.append("?")

        result = ''.join(array_trad)
        return{
            "dictionnary_name":dictionnary_name.name,
            "word":traduction.word,
            "traduction": result
            } 
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        raise
   

