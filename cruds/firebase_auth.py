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

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

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

        firebase_user = ''
        try:
            firebase_user = auth.verify_id_token(token.credentials)

        except Exception as e:
            print(e)
            raise credentials_exception

        user_id: UserId = UserId(google_uid=firebase_user['user_id'])
        # if user is None:
        #     raise credentials_exception
        print(user_id)
        return user_id