from app.services.neo4j_service import run_query

def create_profile_picture(user_id: str, media_url: str):
    query = """
MATCH (u:User {id: $user_id})
OPTIONAL MATCH (u)-[r:HAS_PROFILE_PICTURE]->(oldP:ProfilePicture)
DELETE r, oldP
CREATE (newP:ProfilePicture {
    id: randomUUID(),
    media_url: $media_url,
    created_at: datetime()
})
CREATE (u)-[:HAS_PROFILE_PICTURE]->(newP)
RETURN newP AS p, u

    """
    result = run_query(query, {"user_id": user_id, "media_url": media_url}, single=True)
    if not result:
        return None
    return {
        "user_id": result["u"]["id"],
        "profile_picture": {
            "id": result["p"]["id"],
            "media_url": result["p"]["media_url"],
            "created_at": str(result["p"]["created_at"])
        }
    }
