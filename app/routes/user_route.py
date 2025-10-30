from fastapi import APIRouter, HTTPException, Depends
from app.controllers.user_controller import get_user_by_id, delete_user
from app.schemas.user_schema import UserResponse, UserCreate
from app.auth import get_current_user
from fastapi import APIRouter, HTTPException, Query
from app.controllers.user_controller import search_users_controller, test_connection_controller
from app.services.neo4j_service import get_driver 
from fastapi import APIRouter, Query, HTTPException
# make sure this points to your driver setup

router = APIRouter(prefix="/users", tags=["Users login and sign up"])
active_users = set()

@router.post("/online")
def mark_online(current_user: str = Depends(get_current_user)):
    """Mark a user as online."""
    active_users.add(current_user)
    print(f"✅ User {current_user} is now online")
    return {"status": "online"}

@router.delete("/online")
def mark_offline(current_user: str = Depends(get_current_user)):
    """Mark a user as offline."""
    active_users.discard(current_user)
    print(f"❌ User {current_user} went offline")
    return {"status": "offline"}

# make sure this import exists

@router.get("/active")
def get_active_users():
    """Return currently active users (with username)."""
    print(f"📡 Active users: {active_users}")

    if not active_users:
        return []

    driver = get_driver()
    query = """
    MATCH (u:User)
    WHERE u.id IN $ids
    RETURN u.id AS id, u.username AS username
    """
    with driver.session() as session:
        result = session.run(query, ids=list(active_users))
        users = [record.data() for record in result]

    print("🟢 Sending active users:", users)
    return users



@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.delete("/{user_id}")
def delete_user_route(user_id: str):
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}




router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/search")
def search_users(query: str = Query(..., description="Search for users by username")):
    driver = get_driver()
    cypher = """
    MATCH (u:User)
    WHERE u.username =~ $pattern
    RETURN u.id AS id, u.username AS username, u.email AS email
    ORDER BY u.username
    LIMIT 20
    """
    pattern = f"(?i).*{query}.*"  # case-insensitive regex

    print("🔍 Using pattern:", pattern)

    try:
        with driver.session() as session:
            result = session.run(cypher, {"pattern": pattern})
            users = [record.data() for record in result]

        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
