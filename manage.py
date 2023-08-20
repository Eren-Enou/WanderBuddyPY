from app import app, db

def create_db():
    """Create database with all tables."""
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    task = input("Enter task name (e.g., 'create_db'): ")
    if task == "create_db":
        create_db()
    else:
        print(f"No task found for {task}")
