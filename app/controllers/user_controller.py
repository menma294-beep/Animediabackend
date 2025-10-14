from app.services.neo4j_service import get_driver

def get_user_by_id(user_id: str):
    driver = get_driver()
    query = "MATCH (u:User {id: $user_id}) RETURN u"
    with driver.session() as session:
        record = session.run(query, user_id=user_id).single()
        return record["u"] if record else None

def get_all_users():
    driver = get_driver()
    query = "MATCH (u:User) RETURN u"
    with driver.session() as session:
        return [record["u"] for record in session.run(query)]

def update_user(user_id: str, username: str, email: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})
    SET u.username = $username, u.email = $email
    RETURN u
    """
    with driver.session() as session:
        record = session.run(query, user_id=user_id, username=username, email=email).single()
        return record["u"] if record else None

def delete_user(user_id: str):
    driver = get_driver()
    query = "MATCH (u:User {id: $user_id}) DETACH DELETE u"
    with driver.session() as session:
        session.run(query, user_id=user_id)
        return True


# app/controllers/user_controller.py  (add these)


