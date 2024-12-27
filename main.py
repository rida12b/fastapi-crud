from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import text
from typing import Optional

# Connexion à la base de données
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/AdventureWorks?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Initialiser l'application FastAPI
app = FastAPI(
    title="API de gestion des produits",
    description="""
Une API CRUD pour gérer les produits dans une base de données. 

Fonctionnalités disponibles :
- Créer un produit
- Lire les produits (liste ou détail)
- Mettre à jour un produit
- Supprimer un produit
    """,
    version="1.0.0",
    contact={
        "name": "Support API",
        "email": "support@example.com",
    },
)

# Modèle SQLModel pour la table Product
class Product(SQLModel, table=True):
    ProductID: Optional[int] = Field(default=None, primary_key=True)
    Name: str
    ProductNumber: str
    StandardCost: float
    ListPrice: float
    SellStartDate: str


# Route pour la racine "/"
@app.get("/", summary="Page d'accueil", description="Retourne un message de bienvenue.")
def read_root():
    return {"message": "Bienvenue sur votre API FastAPI ! Utilisez /docs pour explorer les endpoints."}


# Route pour configurer la base de données
@app.get(
    "/setup-database",
    summary="Configurer la base de données",
    description="Crée la table Product si elle n'existe pas déjà.",
    response_description="Un message confirmant la configuration."
)
def setup_database():
    with Session(engine) as session:
        try:
            # Créer la table Product si elle n'existe pas
            session.execute(text("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Product' AND xtype='U')
                CREATE TABLE Product (
                    ProductID INT PRIMARY KEY IDENTITY(1,1),
                    Name NVARCHAR(100) NOT NULL,
                    ProductNumber NVARCHAR(50) NOT NULL,
                    StandardCost FLOAT NOT NULL,
                    ListPrice FLOAT NOT NULL,
                    SellStartDate DATETIME NOT NULL
                );
            """))
            session.commit()
            return {"message": "Base de données configurée avec succès."}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Erreur lors de la configuration : {str(e)}")


# Route pour lister tous les produits
@app.get(
    "/products",
    summary="Lister tous les produits",
    description="Retourne une liste de tous les produits présents dans la base de données.",
    response_description="Une liste d'objets Produit."
)
def list_products():
    with Session(engine) as session:
        result = session.exec(select(Product)).all()
        if not result:
            return {"message": "Aucun produit trouvé dans la base de données."}
        return result


# Route pour créer un produit
@app.post(
    "/products",
    summary="Créer un produit",
    description="Ajoute un produit à la base de données avec les informations fournies.",
    response_description="L'objet Produit créé.",
    status_code=201
)
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


# Route pour mettre à jour un produit
@app.put(
    "/products/{product_id}",
    summary="Mettre à jour un produit",
    description="Met à jour les informations d'un produit existant en fonction de son ID.",
    response_description="L'objet Produit mis à jour."
)
def update_product(product_id: int, product: Product):
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Produit non trouvé")
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        session.commit()
        session.refresh(db_product)
        return db_product


# Route pour supprimer un produit
@app.delete(
    "/products/{product_id}",
    summary="Supprimer un produit",
    description="Supprime un produit existant en fonction de son ID.",
    response_description="Un message confirmant la suppression.",
    status_code=204
)
def delete_product(product_id: int):
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Produit non trouvé")
        session.delete(db_product)
        session.commit()
        return {"message": f"Produit avec ID {product_id} supprimé."}
