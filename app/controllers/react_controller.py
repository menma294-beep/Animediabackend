from app.services.neo4j_service import get_driver
import uuid, datetime

def create_react(user_id: str, target_id: str, react_type: str):
    driver = get_driver()
    react_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat()

    query = """
    MATCH (u:User {id: $user_id})
    MATCH (target) WHERE target.id = $target_id AND (target:Post OR target:Comment)
    CREATE (r:React {id: $react_id, type: $react_type, created_at: $created_at})
    MERGE (u)-[:REACTED]->(r)
    MERGE (r)-[:ON]->(target)
    RETURN r, u, target
    """
    with driver.session() as session:
        result = session.run(
            query, user_id=user_id, target_id=target_id,
            react_id=react_id, react_type=react_type, created_at=created_at
        )
        record = result.single()
        return {"react": record["r"], "user": record["u"], "target": record["target"]}

def get_reacts_for_target(target_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User)-[:REACTED]->(r:React)-[:ON]->(target {id: $target_id})
    RETURN r, u, target
    ORDER BY r.created_at ASC
    """
    with driver.session() as session:
        result = session.run(query, target_id=target_id)
        return [{"react": record["r"], "user": record["u"], "target": record["target"]} for record in result]
