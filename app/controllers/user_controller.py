from app.services.neo4j_service import get_driver

def get_user_by_id(user_id: str):
    driver = get_driver()
    query = "MATCH (u:User {id: $user_id}) RETURN u"
    with driver.session() as session:
        record = session.run(query, user_id=user_id).single()
        return record["u"] if record else None



def delete_user(user_id: str):
    driver = get_driver()
    query = "MATCH (u:User {id: $user_id}) DETACH DELETE u"
    with driver.session() as session:
        session.run(query, user_id=user_id)
        return True


from fastapi import HTTPException


def search_users_controller(query: str):
    driver = get_driver()
    cypher = """
    MATCH (u:User)
    WHERE u.username =~ $pattern
    RETURN u.id AS id, u.username AS username, u.email AS email
    ORDER BY u.username
    LIMIT 20
    """
    pattern = f"(?i).*{query}.*"  # Case-insensitive regex
    print("🔍 Pattern used:", pattern)  # <-- Add this for debugging

    try:
        with driver.session() as session:
            result = session.run(cypher, {"pattern": pattern})
            users = [record.data() for record in result]

        print("✅ Found users:", users)  # <-- Add this too

        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def test_connection_controller():
    print("✅ Controller reached! I'm here.")  # This should print in the terminal
    return {"message": "Controller is working!"}
