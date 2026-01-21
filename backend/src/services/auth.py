from passlib.hash import argon2
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import os


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET", "your-super-secret-jwt-signing-key-change-this-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    def hash_password(self, password: str) -> str:
        """Hash a password using Argon2.

        Args:
            password: Plaintext password to hash

        Returns:
            Hashed password string
        """
        return argon2.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plaintext password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        try:
            return argon2.verify(plain_password, hashed_password)
        except Exception:
            return False

    def create_access_token(self, user_id: UUID, email: str) -> str:
        """Create a JWT access token.

        Args:
            user_id: User's UUID
            email: User's email address

        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(hours=self.jwt_expiration_hours)
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "iat": datetime.utcnow(),
            "exp": expire,
        }
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError:
            return None

    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Validate password meets security requirements.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"

        return True, ""


# Create singleton instance
auth_service = AuthService()
