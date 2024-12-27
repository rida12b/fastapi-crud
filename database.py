from sqlmodel import create_engine

# URL de connexion à votre base de données AdventureWorks
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/AdventureWorks?driver=ODBC+Driver+17+for+SQL+Server"

# Configuration du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

