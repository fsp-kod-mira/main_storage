from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from config import *

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
    id_feature = Column(Integer, ForeignKey('features.id'), nullable=False)
    id_template = Column(Integer, ForeignKey('templates.id'), nullable=False) 

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


CreateTables()