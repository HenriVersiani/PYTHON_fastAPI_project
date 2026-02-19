from app.repository import create_user, get_users

def create_user_service(db, user):
    #validaçoes se quiser aqyui.
    return create_user(db, user)


def list_users_service(db):
    return get_users(db)
