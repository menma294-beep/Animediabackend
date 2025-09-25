from app.services.neo4j_service import get_driver
import uuid, datetime

def create_comment(user_id: str, post_id: str, content: str):
    driver = get_driver()
    comment_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat()

    query = """
    MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
    CREATE (c:Comment {id: $comment_id, content: $content, created_at: $created_at})
    MERGE (u)-[:WROTE]->(c)
    MERGE (c)-[:ON_POST]->(p)
    RETURN c, u, p
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id, post_id=post_id, comment_id=comment_id, content=content, created_at=created_at)
        record = result.single()
        return {"comment": record["c"], "user": record["u"], "post": record["p"]}

def get_comments_for_post(post_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User)-[:WROTE]->(c:Comment)-[:ON_POST]->(p:Post {id: $post_id})
    RETURN c, u, p
    ORDER BY c.created_at ASC
    """
    with driver.session() as session:
        result = session.run(query, post_id=post_id)
        return [{"comment": record["c"], "user": record["u"], "post": record["p"]} for record in result]
