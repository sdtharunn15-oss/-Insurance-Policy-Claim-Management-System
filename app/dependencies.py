from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user


def admin_required(current_user=Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


def agent_required(current_user=Depends(get_current_user)):
    if current_user.role not in ["Admin", "Insurance Agent"]:
        raise HTTPException(
            status_code=403,
            detail="Insurance Agent access required"
        )
    return current_user


def customer_required(current_user=Depends(get_current_user)):
    if current_user.role != "Customer":
        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )
    return current_user