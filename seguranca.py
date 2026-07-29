from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

pwd_context = PasswordHash((BcryptHasher(),))

def gerar_hash_senha(senha_texto: str) -> str:

    return pwd_context.hash(senha_texto)

def verificar_senha(senha_texto_puro: str, senha_hash_banco: str) -> bool:

    return pwd_context.verify(senha_texto_puro, senha_hash_banco)