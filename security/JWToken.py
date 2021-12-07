from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, status
from schemas.token_schemas import TokenDataSchema
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models.all import User, UserRole, Role, RolePermission, Permission


from database import db_conn


from datetime import datetime, timedelta

get_db = db_conn.get_db
SECRET_KEY = "dsfdsfhgdsakjfhygdskjhckjdshckjdesgd4387tr874tfc74ri743qtydfi743tyrfoc43ty"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

# Tokenizer ////////////////////////////
def create_access_token(data:dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
        return token_data
    except JWTError:
        raise credentials_exception
# /////////////////////////////////////


# Oauthrizer /////////////////////////
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):

    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
        )
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(
        User.username == token_data.username).first() 

    if not user:
        raise credentials_exception
    if security_scopes.scopes and not token_data.role:
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    if (
        security_scopes.scopes
        and token_data.role not in security_scopes.scopes
    ):
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return user


class Roler():
    def role(user_id, db, key):
        user_roles = db.query(UserRole).filter(User.id == user_id).all()
        keys = []
        for i in user_roles:
            permission_id = db.query(RolePermission).filter(Role.id == i.role_id).first().permission_id
            keys.append(db.query(Permission).filter(Permission.id == permission_id).first().key)
        if key in keys:
            return True
        return False