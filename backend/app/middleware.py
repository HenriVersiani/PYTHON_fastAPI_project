import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class SimpleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user_id = request.headers.get("X-User-Id")
        request.state.username = request.headers.get("X-Username") #contexto do usuario
        request.state.role = request.headers.get("X-User-Role", "user")
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        print(
            f"{request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- {process_time:.3f}s"
        )
         
        return response

app.add_middleware(SimpleMiddleware)