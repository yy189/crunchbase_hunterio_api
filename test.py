import crunchbase_db

if __name__ == "__main__":
    crunchbase_db.restart_mongodb_service()
    crunchbase_db.injest_companies()
    crunchbase_db.save_db()
    crunchbase_db.stop_mongodb_service()