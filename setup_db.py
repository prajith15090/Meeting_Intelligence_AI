from database.db import engine
from database.models import Base
from sqlalchemy import text

with engine.connect() as conn:
    # Drop old table if exists
    conn.execute(text("DROP TABLE IF EXISTS meeting_history CASCADE;"))
    # In case we need to drop the new ones to be sure
    conn.execute(text("DROP TABLE IF EXISTS followups CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS action_items CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS meetings CASCADE;"))
    conn.commit()

Base.metadata.create_all(bind=engine)
print("Database schema updated successfully.")
