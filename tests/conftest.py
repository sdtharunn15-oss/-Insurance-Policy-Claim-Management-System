
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

from app.models.user import User
from app.utils import get_password_hash
from app.utils import create_access_token


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_insurance.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)



@pytest.fixture()
def db(db_engine):

    connection = db_engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    yield session

    session.close()

    transaction.rollback()

    connection.close()



@pytest.fixture()
def client(db):

    def override_get_db():

        try:
            yield db

        finally:
            pass


    app.dependency_overrides[get_db] = override_get_db


    with TestClient(app) as c:
        yield c


    app.dependency_overrides.clear()



@pytest.fixture()
def create_users(db):

    admin = User(
        name="Admin User",
        email="admin@test.com",
        password=get_password_hash("admin123"),
        role="Admin"
    )


    agent = User(
        name="Agent User",
        email="agent@test.com",
        password=get_password_hash("agent123"),
        role="Insurance Agent"
    )


    customer = User(
        name="Customer User",
        email="customer@test.com",
        password=get_password_hash("customer123"),
        role="Customer"
    )


    db.add_all(
        [
            admin,
            agent,
            customer
        ]
    )

    db.commit()


    db.refresh(admin)
    db.refresh(agent)
    db.refresh(customer)


    return {
        "admin": admin,
        "agent": agent,
        "customer": customer
    }



@pytest.fixture()
def admin_token(create_users):

    user = create_users["admin"]

    return create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )



@pytest.fixture()
def agent_token(create_users):

    user = create_users["agent"]

    return create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )



@pytest.fixture()
def customer_token(create_users):

    user = create_users["customer"]

    return create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )