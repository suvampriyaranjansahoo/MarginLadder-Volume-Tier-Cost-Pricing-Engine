"""Password hashing and session tokens (standard library only).

Passwords use scrypt with a random salt. Session tokens are random and stored only as
SHA-256 hashes, so a stolen database does not hand out working sessions.
This is local-demo grade: no password reset, no MFA, no TLS termination. See docs/architecture.md.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets

MIN_PASSWORD_LENGTH = 10
_N, _R, _P = 2 ** 14, 8, 1


def hash_password(password: str) -> str:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must have at least {MIN_PASSWORD_LENGTH} characters")
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P)
    return f"scrypt${_N}${_R}${_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, n, r, p, salt_hex, digest_hex = stored.split("$")
        if scheme != "scrypt":
            return False
        digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=int(n), r=int(r), p=int(p))
        return hmac.compare_digest(digest, bytes.fromhex(digest_hex))
    except (ValueError, TypeError):
        return False


def new_token() -> str:
    return secrets.token_urlsafe(32)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
