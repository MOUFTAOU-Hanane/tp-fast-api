from sqlalchemy.orm import Session
from ..import models, schemas
from ..models.Dictionnary import Dictionnary
from ..models.Traduction import Traduction
from ..schemas.schema import DictionnaryIn, DictionnaryOut, TraductionIn, TraductionWordIn



def get_dictionary(db: Session, dictionnary_id: int):
    return db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()


def get_dictionnary_by_name(db: Session, name: str):
    return db.query(Dictionnary).filter(Dictionnary.name == name).first()


def get_dictionaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dictionnary).offset(skip).limit(limit).all()


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




def get_traduction(db: Session, traduction_id: int):
    return db.query(Traduction).filter(Traduction.id == traduction_id).first()

def get_traductions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Traduction).offset(skip).limit(limit).all()

def create_traduction(db: Session, traduction_create: TraductionIn):
    traductions = []

    # Pour chaque ligne dans traduction_create.lines
    for line_create in traduction_create.lines:
        # Créer l'objet Traduction
        traduction = Traduction(
            key=line_create.key,
            value=line_create.value,
            dictionnary_id=traduction_create.dictionnary_id
        )

        db.add(traduction)
        traductions.append(traduction)

    db.commit()

    return traductions 


# def update_traduction(db: Session, traduction: TraductionIn, traduction_id: int):
#     traduction_in_db = db.query(Traduction).filter(Traduction.id == traduction_id).first()

#     # Mettre à jour les champs de Traduction avec les valeurs de TraductionIn
#     traduction_in_db.dictionnary_id = traduction.dictionnary_id

#     # Effacer les lignes existantes associées à cette traduction
#     db.query(Line).filter(Line.translation_id == traduction_id).delete()

#     # Ajouter les nouvelles lignes
#     for line_create in traduction.lines:
#         line = Line(key=line_create.key, value=line_create.value)
#         traduction_in_db.lines.append(line)
#         db.add(line)

#     # Commit des modifications dans la base de données
#     db.commit()

#     # Rafraîchir l'objet traduction
#     db.refresh(traduction_in_db)

#     return traduction_in_db
def traduction_word(db: Session, traduction):
    try:
        array_trad = []
        word = traduction.word
        for item in word:
            translation = db.query(Traduction).filter(Traduction.key == item, Traduction.dictionnary_id == traduction.dictionnary_id).first()
            if translation:
                array_trad.append(translation.value)
            else:
                array_trad.append("?")

        result = ''.join(array_trad)
        return result
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        raise
   

