from orator import DatabaseManager, Schema, Model

DATABASES = {
    "mysql": {
        "driver": "mysql",
        "host": "c6156-nfl-searching-query-microservice-db.ckoq7q2zprcp.us-east-2.rds.amazonaws.com",
        "database": "dbNFLstat",
        "user": "tw6156",
        "password": "linguine_falafel_pita",
        "prefix": "",
        "port": 3306,
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)