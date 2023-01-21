from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.params import Security
from fastapi.security import HTTPBearer
from fastapi import Depends, status
from db import get_db
# from fastapi.security import OAuth2PasswordBearer
from schemas.user import UserId

oauth2_scheme = HTTPBearer()

class GetCurrentUser:
    def __init__(self) -> None:
        self.auto_error = ''

    def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Colud not validate credentials',
            headers={'WWW-Authenticate': "Bearer"}
        )
        # try:

        # except JWTError:
        #     raise credentials_exception
        
        # user = db_user.get_user_by_username(db, username)
        user_id: UserId = UserId(google_uid="hoge")
        # if user is None:
        #     raise credentials_exception
        return user_id