from app.services.neo4j_service import get_driver
from app.controllers.notification_controller import create_notification
def follow_user(follower_id: str, followee_id: str):
    driver = get_driver()
    query = """
    MATCH (follower:User {id: $follower_id}), (followee:User {id: $followee_id})
    MERGE (follower)-[:FOLLOWS]->(followee)
    RETURN follower, followee
    """
    with driver.session() as session:
        record = session.run(
            query,
            follower_id=follower_id,
            followee_id=followee_id
        ).single()

        if not record:
            print("⚠️ No record returned from follow action.")
            return None

        print(f"👥 {follower_id} followed {followee_id}")

        # 🔔 Create notification for the followee
        if follower_id != followee_id:
            create_notification(
                sender_id=follower_id,
                receiver_id=followee_id,
                message="Started following you.",
                notif_type="follows",
                target_id=follower_id,  # ✅ link to follower (the sender)
                target_type="user"
            )
            print("✅ Notification created for follow.")
        else:
            print("🟡 Skipping notif — user cannot follow themselves.")

        return {
            "follower": {
                "id": record["follower"]["id"],
                "username": record["follower"]["username"]
            },
            "followee": {
                "id": record["followee"]["id"],
                "username": record["followee"]["username"]
            }
        }

def get_followers(user_id: str):
    driver = get_driver()
    query = """
    MATCH (follower:User)-[:FOLLOWS]->(u:User {id: $user_id})
    RETURN follower
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        return [record["follower"] for record in result]

