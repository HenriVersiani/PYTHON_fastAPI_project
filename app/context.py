from fastapi import Request


def get_user_context(request: Request):
    return {
        "user_id": getattr(request.state, "user_id", None),
        "username": getattr(request.state, "username", None)
    }
