from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from app.auth import verify_token

security = HTTPBearer()

def get_current_user(credentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = verify_token(token)
        user_id = int(payload.get("sub"))
        email = payload.get("email")
        role = payload.get("role", "user")
        
        return {
            "user_id": user_id,
            "email": email,
            "role": role
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_user(user: dict = Depends(get_current_user)) -> dict:
    if not user.get("user_id"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

