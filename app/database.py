import os
from sqlalchemy import create_engine, update, delete, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.dialects.postgresql import array
from app.model import RecipeSchema

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ingredients = Column(ARRAY(String))

def save_recipe(db: Session, recipe: RecipeSchema) -> dict:
    recipe_entity = Recipe(name=recipe.name, ingredients=array(recipe.ingredients))
    db.add(recipe_entity)
    db.commit()
    db.refresh(recipe_entity)
    return {
        "id": recipe_entity.id
    }

def get_single_recipe(db: Session, id: int) -> dict:
    return db.query(Recipe).filter(Recipe.id == id).first()

def get_all_recipes(db: Session) -> list:
    return db.query(Recipe).all()

def update_recipe_data(db: Session, id: int, data: dict):
    db.execute(
        update(Recipe).
        where(Recipe.id == id).
        values(**data)
    )
    db.commit()

def remove_recipe(db: Session, id: int):
    db.execute(
        delete(Recipe).
        where(Recipe.id == id)
    )
    db.commit()
