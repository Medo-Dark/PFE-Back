from config.database import SessionLocal, SessionLocalData


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_data():
    db = SessionLocalData()
    try:
        yield db
    finally:
        db.close()
