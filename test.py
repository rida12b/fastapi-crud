from sqlmodel import create_engine, Session
from sqlalchemy import text

# Connexion à la base de données
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/AdventureWorks?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Création de la table et insertion des données
with Session(engine) as session:
    try:
        # Créer la table Product
        session.execute(text("""
            CREATE TABLE Product (
                ProductID INT PRIMARY KEY IDENTITY(1,1),
                Name NVARCHAR(100) NOT NULL,
                ProductNumber NVARCHAR(50) NOT NULL,
                StandardCost FLOAT NOT NULL,
                ListPrice FLOAT NOT NULL,
                SellStartDate DATETIME NOT NULL
            );
        """))
        print("Table 'Product' créée avec succès.")

        # Insérer des données dans la table
        session.execute(text("""
            INSERT INTO Product (Name, ProductNumber, StandardCost, ListPrice, SellStartDate)
            VALUES 
            ('Produit A', 'PROD-001', 50.0, 75.0, GETDATE()),
            ('Produit B', 'PROD-002', 30.0, 50.0, GETDATE()),
            ('Produit C', 'PROD-003', 20.0, 40.0, GETDATE());
        """))
        session.commit()
        print("Données insérées avec succès.")
    except Exception as e:
        print("Erreur :", e)
