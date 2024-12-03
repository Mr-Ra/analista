from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status


from contextlib import asynccontextmanager
from auth.routers import auth_router
from files.routers import files_router
from events.routers import events_router



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los or├¡genes. Cambia "*" por una lista espec├¡fica si es necesario.
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Permitir todos los m├®todos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)



app.include_router(
    router=auth_router,
    prefix=f"/api/auth",
    tags=["auth-register"]
)


app.include_router(
    router=files_router,
    prefix=f"/api/file",
    tags=["file"]
)


app.include_router(
    router=events_router,
    prefix=f"/api/events",
    tags=["events"]
)
