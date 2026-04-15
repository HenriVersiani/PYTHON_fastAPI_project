from app.database import engine, SessionLocal
from app.models import Base, Role
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        try:
            stmt = select(Role)
            existing_roles = db.scalars(stmt).all()
            
            if not existing_roles:
                user_role = Role(id=1, name="user")
                admin_role = Role(id=2, name="admin")
                
                db.add(user_role)
                db.add(admin_role)
                db.commit()
                print("✓ Roles inicializadas: user (1) e admin (2)")
            else:
                print(f"✓ Roles já existem: {[role.name for role in existing_roles]}")
        finally:
            db.close()
    except OperationalError as e:
        print("⚠ Aviso: PostgreSQL não está rodando. Inicie o banco de dados.")
        print(f"  Erro: {str(e).split(chr(10))[0]}")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {str(e)}")

if __name__ == "__main__":
    init_db()
