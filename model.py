from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from config import *
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError


Base = declarative_base()
engine = create_engine(psql_conn_url)



class Feature(Base):
    """
    Модель таблицы features.
    Представляет собой функциональность с приоритетом и связана с несколькими шаблонами.
    """
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)   
    priority_id = Column(Integer, ForeignKey('priorities.id'), nullable=False)

    # Отношение многие-к-одному с таблицей Priority
    priorities = relationship("Priority", back_populates="feature")
    # Отношение многие-ко-многим с таблицей Template через таблицу FeaturesTemplates
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

    # Отношение многие-ко-многим с таблицей Feature через таблицу FeaturesTemplates
    features = relationship("FeaturesTemplates", back_populates="template")


class FeaturesTemplates(Base):
    """
    Модель таблицы features_templates.
    Связывает таблицы Feature и Template для реализации отношения многие-ко-многим.
    """
    __tablename__ = 'features_templates'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False) 

    # Отношение многие-к-одному с таблицей Feature
    feature = relationship("Feature", back_populates="templates")
    # Отношение многие-к-одному с таблицей Template
    template = relationship("Template", back_populates="features")


class Priority(Base):
    """
    Модель таблицы priorities.
    Представляет собой приоритет, который связан с несколькими функциональностями.
    """
    __tablename__ = 'priorities'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String(255), nullable=False)

    # Отношение один-ко-многим с таблицей Feature
    feature = relationship("Feature", back_populates="priorities")


def CreateTables():
    Base.metadata.create_all(engine)

def GetSession():
    Session = sessionmaker(bind=engine)
    return Session()

CreateTables()



class ModelException(Exception):
    pass





def AddTemplate(name, description=None):
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
        

def AddFeatureTemplateLink(feature_id, template_id):
    """
    Добавляет связь между функциональностью и шаблоном в базу данных и возвращает id новой записи.
    """
    with GetSession() as session:
        res = session.query(FeaturesTemplates).filter(FeaturesTemplates.id == template_id, FeaturesTemplates.feature_id == feature_id).first()
        if res:
            print(f"Запись уже имеется, скипаем feature_id: {feature_id}, template_id: {template_id}")
            return

        try:
            feature_template = FeaturesTemplates(feature_id=feature_id, template_id=template_id)
            session.add(feature_template)
            session.commit()
            return feature_template.id
        except IntegrityError:
            session.rollback()
            return None
        






def UpdateTemplateFeaturesLink(link_id, template_id, feature_id):
    """
    Обновление связи между шаблоном и фичей
    """
    with GetSession() as session:
        res = session.query(Template).filter(Template.id == template_id).first()
        if res:
            res.template_id = template_id
            res.feature_id = feature_id
            session.commit()
        else:
            raise ModelException("Не найдена структура")


def UpdateTemplate(template_id, name, description):
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






def GetFeaturesByTemplateId(template_id):
    """
    Получение всех функциональностей по идентификатору шаблона.
    """
    features_dicts = []
    with GetSession() as session:
        
        links = session.query(FeaturesTemplates).filter(FeaturesTemplates.template_id == template_id).all()
        
        for link in links:
            feature = session.query(Feature).filter(Feature.id == link.feature_id).first()
            if feature:
                feature_dict = {
                    "id": feature.id,
                    "name": feature.name,
                    "priority_id": feature.priority_id
                }
                features_dicts.append(feature_dict)
        return features_dicts

        












def DeleteFeatureTemplateLink(feature_id, template_id):
    """
    Удаляет связь меду функциональностью и шаблоном в базе данных
    """
    with GetSession() as session:
        res = session.query(FeaturesTemplates).filter(FeaturesTemplates.template_id == template_id, FeaturesTemplates.feature_id == feature_id).first()
        if res:
            session.delete(res)
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
