from fastapi import FastAPI

from app.database import Base, engine

from app.routers.auth import router as auth_router
from app.routers.customers import router as customer_router
from app.routers.policies import router as policy_router
from app.routers.claims import router as claim_router
from app.routers.reports import router as report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Insurance Policy & Claims Management System",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(policy_router)
app.include_router(claim_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {
        "message": "Insurance Policy & Claims Management API is running"
    }