from fastapi import Request, HTTPException


def get_user_context(request: Request):
    return {
        "user_id": getattr(request.state, "user_id", None),
        "username": getattr(request.state, "username", None),
        "role": getattr(request.state, "role", "user")
    }


def require_admin(request: Request):
    context = get_user_context(request)
    if context["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return context


def require_user(request: Request):
    context = get_user_context(request)
    if not context["user_id"]:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return context
