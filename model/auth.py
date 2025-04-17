import jwt
import os

class TokenModel:
    access_token: str
    token_type: str

    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type

    @staticmethod
    def decode_token(access_token: str) -> str:
        acem = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        sk = os.getenv("SECRET_KEY")
        al = os.getenv("ALGORITHM")

        if acem and sk and al:
            payload = jwt.decode(access_token, sk, algorithms=[al])
            user_uuid = payload.get("sub")
            return user_uuid

        else:
            raise FileNotFoundError(
                ".env파일에서 ACCESS_TOKEN_EXPIRE_MINUTES과 SECRET_KEY 환경 변수를 찾을 수 없습니다!"
            )
