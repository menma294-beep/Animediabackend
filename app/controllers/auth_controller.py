import uuid
from datetime import datetime, timedelta
import jwt
from app.services.neo4j_service import get_driver
from app.config import settings

# JWT settings
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Signup
def signup_user(username: str, email: str, password: str):
    driver = get_driver()
    user_id = str(uuid.uuid4())
    query = """
    CREATE (u:User {id: $user_id, username: $username, email: $email, password: $password, last_active: datetime()})
    RETURN u
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id, username=username, email=email, password=password)
        user = result.single()["u"]

    return create_access_token(data={"sub": user["id"]})

# Login
def login_user(username: str, password: str):
    driver = get_driver()
    query = "MATCH (u:User {username: $username, password: $password}) RETURN u"
    with driver.session() as session:
        record = session.run(query, username=username, password=password).single()
        if not record:
            return None
        user = record["u"]

    return create_access_token(data={"sub": user["id"]})
