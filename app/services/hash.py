import hashlib
from passlib.context import CryptContext


class HashService:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        sha_pass = hashlib.sha256(password.encode()).digest()
        return self.pwd_context.hash(sha_pass)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        sha_password = hashlib.sha256(plain_password.encode()).hexdigest()
        return self.pwd_context.verify(sha_password, hashed_password)
