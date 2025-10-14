
from app.services.neo4j_service import get_driver
import datetime

def create_notification(sender_id: str, receiver_id: str, message: str, notif_type: str, target_id=None, target_type=None):
    driver = get_driver()
    created_at = datetime.datetime.utcnow().isoformat()

    query = """
    MATCH (sender:User {id: $sender_id})
    MATCH (receiver:User {id: $receiver_id})
    CREATE (n:Notification {
        id: randomUUID(),
        message: $message,
        type: $notif_type,
        target_id: $target_id,
        target_type: $target_type,
        created_at: $created_at,
        is_read: false
    })
    MERGE (sender)-[:SENT_NOTIFICATION]->(n)
    MERGE (receiver)-[:RECEIVED_NOTIFICATION]->(n)
    RETURN n, sender.id AS sender_id, receiver.id AS receiver_id, sender.username AS sender_username
    """

    with driver.session() as session:
        result = session.run(query, {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "notif_type": notif_type,
            "target_id": target_id,
            "target_type": target_type,
            "created_at": created_at
        })
        record = result.single()
        if not record:
            return None

        n = record["n"]
        return {
            "id": n["id"],
            "sender_id": record["sender_id"],
            "receiver_id": record["receiver_id"],
            "sender_username": record["sender_username"],
            "message": n["message"],
            "type": n["type"],
            "target_id": n.get("target_id"),
            "target_type": n.get("target_type"),
            "created_at": n["created_at"],
            "is_read": n["is_read"]
        }


def get_notifications_for_user(user_id: str):
    driver = get_driver()
    query = """
    MATCH (receiver:User {id: $user_id})-[:RECEIVED_NOTIFICATION]->(n:Notification)
    OPTIONAL MATCH (sender:User)-[:SENT_NOTIFICATION]->(n)
    RETURN n, sender.id AS sender_id, receiver.id AS receiver_id, sender.username AS sender_username
    ORDER BY n.created_at DESC
    """

    with driver.session() as session:
        result = session.run(query, {"user_id": user_id})
        notifications = []
        for record in result:
            n = record["n"]
            notifications.append({
                "id": n["id"],
                "sender_id": record.get("sender_id"),
                "receiver_id": record.get("receiver_id"),
                "sender_username": record.get("sender_username"),
                "message": n["message"],
                "type": n["type"],
                "target_id": n.get("target_id"),
                "target_type": n.get("target_type"),
                "created_at": n["created_at"],
                "is_read": n["is_read"]
            })
        return notifications

def mark_notification_as_read(notification_id: str):
    driver = get_driver()
    query = """
    MATCH (n:Notification {id: $notification_id})
    SET n.is_read = true
    RETURN n
    """
    with driver.session() as session:
        result = session.run(query, {"notification_id": notification_id})
        record = result.single()
        return record["n"] if record else None
