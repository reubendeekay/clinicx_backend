from .routers import branch, user, auth, doctor, patient, appointment, service, payment

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    description="Clinic X API",
    title="Clinic X API",
    version="1.0.0",
    summary="This is the Clinic X API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Dependency injection


app.include_router(router=branch.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=doctor.router)
app.include_router(router=patient.router)
app.include_router(router=appointment.router)
app.include_router(router=service.router)
app.include_router(router=payment.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Clinic X API"}
