from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.model import RecipeSchema, UpdateRecipeSchema
from app.database import save_recipe, get_all_recipes, get_single_recipe, update_recipe_data, remove_recipe, Base, SessionLocal, engine
from fastapi.responses import RedirectResponse


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def get_root() -> dict:
    return RedirectResponse(url="/docs")

@app.get("/recipe", tags=["Recipe"])
def get_recipes(db: Session = Depends(get_db)) -> dict:
    recipes = get_all_recipes(db)
    return {
        "data": recipes
    }

@app.get("/recipe/{id}", tags=["Recipe"])
def get_recipe(id: int, db: Session = Depends(get_db)) -> dict:
    recipe = get_single_recipe(db, id)
    if recipe:
        return {
            "data": recipe
        }
    return {
        "error": "No such recipe with ID {} exist".format(id)
    }

@app.post("/recipe", tags=["Recipe"])
def add_recipe(recipe: RecipeSchema, db: Session = Depends(get_db)) -> dict:
    new_recipe = save_recipe(db, recipe)
    return new_recipe
  
@app.put("/recipe", tags=["Recipe"])
def update_recipe(id: int, recipe_data: UpdateRecipeSchema, db: Session = Depends(get_db))  -> dict:
    if not get_single_recipe(db, id):
        return {
            "error": "No such recipe exist"
        }

    update_recipe_data(db, id, recipe_data.dict())

    return {
        "message": "Recipe updated successfully."
    }

@app.delete("/recipe/{id}", tags=["Recipe"])
def delete_recipe(id: int, db: Session = Depends(get_db)) -> dict:
    if not get_single_recipe(db, id):
        return {
            "error": "Invalid ID passed"
        }


    remove_recipe(db, id)
    return {
        "message": "Recipe deleted successfully."
    }