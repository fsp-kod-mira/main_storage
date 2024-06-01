from sqlalchemy import create_engine, Column, Integer, Text, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum
import logging
import os



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


psql_conn_url = os.getenv('PSQL_URL') or 'postgresql://postgres:postgres@localhost:5432/fichi'


Base = declarative_base()
engine = create_engine(psql_conn_url)


import enum





class Feature(Base):
    """
    Модель таблицы features.
    Представляет собой функциональность с приоритетом и связана с несколькими шаблонами.
    """
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)   
    feature_type = Column(Integer, nullable=False)
    templates = relationship("FeaturesTemplates", back_populates="feature")


class Template(Base):
    """
    Модель таблицы templates.
    Представляет собой шаблон с описанием и связан с несколькими функциональностями.
    """
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String(255), nullable=False)                
    description = Column(String(255))                         
    features = relationship("FeaturesTemplates", back_populates="template")


## ссылки
class FeaturesTemplates(Base):
    """
    Модель таблицы features_templates.
    Связывает таблицы Feature и Template для реализации отношения многие-ко-многим.
    """
    __tablename__ = 'features_templates'
    id = Column(Integer, primary_key=True, autoincrement=True) 
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False) 
    value = Column(Text)

    # Отношение многие-к-одному с таблицей Feature
    feature = relationship("Feature", back_populates="templates")
    # Отношение многие-к-одному с таблицей Template
    template = relationship("Template", back_populates="features")




def CreateTables():
    Base.metadata.create_all(engine)

def GetSession():
    Session = sessionmaker(bind=engine)
    return Session()





class ModelException(Exception):
    pass


















#========================================================================================================================
#                       Реализация интерфейса
#========================================================================================================================



def CreateFeature(name, feature_type):
    """
    Добавление новой фичи
    """
    with GetSession() as session:
        try:
            
            feature = Feature(name=name, feature_type=feature_type)
            session.add(feature)
            session.commit()
            return feature.id
        except IntegrityError:
            session.rollback()
            return None



def UpdateFeature(feature_id, name, feature_type):
    """
    Обновление фичи
    """
    with GetSession() as session:
        try:
            feature = session.query(Feature).filter(Feature.id == feature_id).first()
            feature.name = name
            feature.feature_type = feature_type
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False



def DeleteFeature(feature_id):
    """
    Удаление фичи
    """
    with GetSession() as session:
        try:
            feature = session.query(Feature).filter(Feature.id == feature_id).first()
            session.delete(feature)
        except Exception as e:
            print(e) 



#========================================================================================================================
#                       Links
#========================================================================================================================



def AddTemplateFeatureLink(feature_id, template_id, value):
    """
    Добавляет связь между функциональностью и шаблоном в базу данных и возвращает id новой записи.
    """
    with GetSession() as session:
        res = session.query(FeaturesTemplates).filter(FeaturesTemplates.id == template_id, FeaturesTemplates.feature_id == feature_id).first()
        if res:
            print(f"Запись уже имеется, скипаем feature_id: {feature_id}, template_id: {template_id}")
            return
        try:
            feature_template = FeaturesTemplates(feature_id=feature_id, template_id=template_id, value=value)
            session.add(feature_template)
            session.commit()
            return feature_template.id
        except IntegrityError:
            session.rollback()
            return None



def UpdateTemplateFeaturesLink(link_id, template_id, feature_id, value):
    """
    Обновление связи между шаблоном и фичей
    """
    with GetSession() as session:
        res = session.query(Template).filter(Template.id == template_id).first()
        if res:
            res.template_id = template_id
            res.feature_id = feature_id
            res.value = value
            session.commit()
        else:
            raise ModelException("Не найдена структура")



def DeleteTemplateFeatureLink(feature_id, template_id):
    """
    Удаляет связь меду функциональностью и шаблоном в базе данных
    """
    with GetSession() as session:
        res = session.query(FeaturesTemplates).filter(
                FeaturesTemplates.template_id == template_id,
                FeaturesTemplates.feature_id == feature_id
            ).first()
        if res:
            session.delete(res)
            session.commit()
        else:
            raise ModelException("Не найдена структура")



#========================================================================================================================
#                   Получение различных данных
#========================================================================================================================




def GetFeaturesByTemplateId(template_id):
    """
    Получение всех функциональностей по идентификатору шаблона.
    """
    features_dicts = []
    with GetSession() as session:
        # получаем какие ссылки
        links = session.query(FeaturesTemplates).filter(FeaturesTemplates.template_id == template_id).all()
        
        for link in links:
            feature = session.query(Feature).filter(Feature.id == link.feature_id).first()
            if feature:
                feature_dict = {
                    "id": feature.id,
                    "name": feature.name,
                    "feature_type": feature.feature_type,
                    "link":{
                        "id": link.id,
                        "feature_id": link.feature_id, 
                        "template_id": link.template_id,
                        "value": link.value
                    }
                }
                features_dicts.append(feature_dict)
        return features_dicts







#========================================================================================================================
#                       Templates
#========================================================================================================================




def CreateTemplate(name, description=None):
    """
    Добавляет новый шаблон в базу данных и возвращает его id.
    """
    with GetSession() as session:
        try:
            template = Template(name=name, description=description)
            session.add(template)
            session.commit()
            return template.id
        except IntegrityError:
            session.rollback()
            return None
        


def UpdateTemplate(name, description, template_id):
    """
    Обновление шаблона
    """
    with GetSession() as session:
        res = session.query(Template).filter(Template.id == template_id).first()
        if res:
            res.name = name
            res.description = description
            session.commit()
        else:
            raise ModelException("Не найдена структура")



def DeleteTemplate(template_id):
    """
    Удаляет шаблон
    """
    with GetSession() as session:
        res = session.query(Template).filter(Template.id == template_id).first()
        if res:
            session.delete(res)
            session.commit()
        else:
            raise ModelException("Не найдена структура")



def GetAllTemplates():
    """
    Получение всех шаблонов
    """
    with GetSession() as session:
        templates = []
        templates_result = session.query(Template).all()
        for template in templates_result:
            template_dict = {
                "id": template.id,
                "name": template.name,
                "description": template.description
            }
            templates.append(template_dict)
        return templates




























# Создание таблиц
CreateTables()