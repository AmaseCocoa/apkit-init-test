import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa


def load_keys(user_id: str) -> tuple[rsa.RSAPrivateKey, ed25519.Ed25519PrivateKey]:
    if not os.path.exists(f"./keys/{user_id}"):
        os.mkdir(f"./keys/{user_id}")

    if not os.path.exists(f"./keys/{user_id}/rsa-key.pem"):
        rsa_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=3072
        )
        with open(f"./keys/{user_id}/rsa-key.pem", "wb") as f:
            f.write(
                rsa_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    else:
        with open(f"./keys/{user_id}/rsa-key.pem", "rb") as f:
            rsa_private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
            if not isinstance(rsa_private_key, rsa.RSAPrivateKey):
                raise ValueError("This key is not a RSAPrivateKey")

    if not os.path.exists(f"./keys/{user_id}/ed25519-key.pem"):
        ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        with open(f"./keys/{user_id}/ed25519-key.pem", "wb") as f:
            f.write(
                ed25519_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    else:
        with open(f"./keys/{user_id}/ed25519-key.pem", "rb") as f:
            ed25519_private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
            if not isinstance(ed25519_private_key, ed25519.Ed25519PrivateKey):
                raise ValueError("This key is not a Ed25519PrivateKey")

    return rsa_private_key, ed25519_private_key