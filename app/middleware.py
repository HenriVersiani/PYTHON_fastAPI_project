import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class SimpleLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        print(
            f"{request.method} {request.url.path} " #metodo e caminho
            f"- Status: {response.status_code} " #status da resposta
            f"- {process_time:.3f}s" #tempo que demorou
        )
         
        return response

app.add_middleware(SimpleLoggerMiddleware)  #aplicando geral