from app.services.neo4j_service import get_driver
import uuid

def create_user(username: str, email: str):
    driver = get_driver()
    user_id = str(uuid.uuid4())
    query = """
    CREATE (u:User {id: $id, username: $username, email: $email})
    RETURN u
    """
    with driver.session() as session:
        result = session.run(query, id=user_id, username=username, email=email)
        record = result.single()
        return record["u"]
def get_all_users():
    driver = get_driver()
    query = "MATCH (u:User) RETURN u"
    with driver.session() as session:
        result = session.run(query)
        return [record["u"] for record in result]
    
def create_friendship(user_id: str, friend_id: str):
    driver = get_driver()
    query = """
    MATCH (a:User {id: $user_id}), (b:User {id: $friend_id})
    MERGE (a)-[:FRIENDS_WITH]->(b)
    RETURN a, b
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id, friend_id=friend_id)
        record = result.single()
        if record:
            return {"user": record["a"], "friend": record["b"]}
        return None
def get_user_friends(user_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]->(f:User)
    RETURN f
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        return [record["f"] for record in result]
