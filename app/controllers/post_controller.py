from app.services.neo4j_service import get_driver
import uuid, datetime

def create_post(user_id: str, content: str):
    driver = get_driver()
    post_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat()

    query = """
    MATCH (u:User {id: $user_id})
    CREATE (p:Post {id: $post_id, content: $content, created_at: $created_at})
    MERGE (u)-[:AUTHORED]->(p)
    RETURN p, u
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id, post_id=post_id, content=content, created_at=created_at)
        record = result.single()
        return {"post": record["p"], "user": record["u"]}

def get_all_posts():
    driver = get_driver()
    query = """
    MATCH (u:User)-[:AUTHORED]->(p:Post)
    RETURN p, u
    ORDER BY p.created_at DESC
    """
    with driver.session() as session:
        result = session.run(query)
        return [{"post": record["p"], "user": record["u"]} for record in result]
def get_posts_by_user(user_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})-[:AUTHORED]->(p:Post)
    RETURN p, u
    ORDER BY p.created_at DESC
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        return [{"post": record["p"], "user": record["u"]} for record in result]
