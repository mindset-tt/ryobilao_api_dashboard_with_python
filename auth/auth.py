import jwt
from datetime import timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'cairocoders-ednalan'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, public_id):
        payload = {'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=12), 'iat': datetime.now(timezone.utc), 'public_id': public_id}


        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['empId']
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail='Signature has expired') from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token') from e

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)