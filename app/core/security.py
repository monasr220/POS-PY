from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime , timedelta , timezone
from typing import Any , Union,Optional
from jose import JWTError , jwt

from config import settings



pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_str}/auth/login"
)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def get_paasword_hash(password:str)->str:
    return pwd_context.hash(password)

def create_access_token(
    subject:Union[str,Any],expire_delta:Optional[timedelta]=None
)->str:
    if expire_delta:
        expire = datetime.now(timezone.utc) +expire_delta
        
    else:
        expire =datetime.now(timezone.utc)+timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encoded = {"exp":expire,"sub":str(subject),"type":"access"}
    encoded_jwt = jwt.encode(
        to_encoded,settings.secret_key,algorithm=settings.algorithm
    )
    return encoded_jwt
def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """إنشاء Refresh Token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt
def decode_token(token: str) -> Optional[dict]:
    """فك تشفير التوكن والتحقق من صحته"""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None