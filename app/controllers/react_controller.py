from app.services.neo4j_service import get_driver
import uuid, datetime
from app.controllers.notification_controller import create_notification
from app.services.neo4j_service import get_driver



def create_react(user_id: str, target_id: str, react_type: str):
    driver = get_driver()
    created_at = datetime.datetime.utcnow().isoformat()
    print("🔥 create_react triggered by:", user_id, "on target:", target_id)

    query = """
    MATCH (u:User {id: $user_id})
    MATCH (target) WHERE target.id = $target_id AND (target:Post OR target:Comment)
    OPTIONAL MATCH (u)-[:REACTED]->(r:React)-[:ON]->(target)
    WITH u, target, r
    CALL apoc.do.when(
        r IS NULL,
        '
        CREATE (newr:React {
            id: randomUUID(),
            type: $react_type,
            created_at: $created_at,
            is_active: true
        })
        MERGE (u)-[:REACTED]->(newr)
        MERGE (newr)-[:ON]->(target)
        RETURN newr AS r, u, target
        ',
        '
        SET r.type = $react_type,
            r.created_at = $created_at,
            r.is_active = true
        RETURN r, u, target
        ',
        {u: u, target: target, r: r, react_type: $react_type, created_at: $created_at}
    ) YIELD value
    RETURN value.r.id AS id, value.r.type AS type, value.r.created_at AS created_at,
           value.u.id AS user_id, value.u.username AS user_username,
           value.target.id AS target_id,
           labels(value.target)[0] AS target_label,
           value.r.is_active AS is_active
    """

    with driver.session() as session:
        record = session.run(
            query,
            user_id=user_id,
            target_id=target_id,
            react_type=react_type,
            created_at=created_at,
        ).single()

        if not record:
            print("⚠️ No record returned from main query.")
            return None

        print("✅ React created or updated successfully.")

        # Determine who owns the post or comment
        target_label = record["target_label"]
        print("🎯 Target label is:", target_label)

        owner_query = f"""
        MATCH (owner:User)-[:AUTHORED]->(target:{target_label} {{id: $target_id}})
        RETURN owner.id AS owner_id
        """
        owner_result = session.run(owner_query, {"target_id": target_id}).single()

        if owner_result:
            receiver_id = owner_result["owner_id"]
            print("👤 Found owner:", receiver_id)

            if receiver_id != user_id:
                print("📨 Creating notification...")
                create_notification(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    message="Reacted on your post." if target_label == "Post" else "Reacted on your comment.",
                    notif_type="reacts",
                    target_id=target_id,
                    target_type=target_label.lower()
                )
                print("✅ Notification creation attempted.")
            else:
                print("🟡 Skipping notif — user reacted to their own post.")
        else:
            print("⚠️ No owner found for target.")

        return {
            "id": record["id"],
            "type": record["type"],
            "created_at": record["created_at"],
            "user_id": record["user_id"],
            "user_username": record["user_username"],
            "target_id": record["target_id"],
            "is_active": record["is_active"]
        }

def set_react_inactive(user_id: str, target_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User {id: $user_id})-[:REACTED]->(r:React {is_active: true})-[:ON]->(target {id: $target_id})
    SET r.is_active = false
    RETURN r.id AS id, r.is_active AS is_active, r.created_at AS created_at,
           u.id AS user_id, u.username AS user_username, target.id AS target_id,
           labels(target)[0] AS target_label
    """
    with driver.session() as session:
        record = session.run(query, user_id=user_id, target_id=target_id).single()

        if not record:
            # no active react found
            return {
                "id": None,
                "is_active": False,
                "created_at": None,
                "user_id": user_id,
                "user_username": None,
                "target_id": target_id,
            }

        # 🔹 Get target label (Post or Comment)
        target_label = record["target_label"]

        # 🔹 Find the owner of that post or comment
        owner_query = f"""
        MATCH (owner:User)-[:AUTHORED]->(target:{target_label} {{id: $target_id}})
        RETURN owner.id AS owner_id
        """
        owner_result = session.run(owner_query, {"target_id": target_id}).single()

        if owner_result:
            receiver_id = owner_result["owner_id"]
            if receiver_id != user_id:
                # 🔔 Create "unliked" notification
                create_notification(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    message="Unliked your post." if target_label == "Post" else "Unliked your comment.",
                    notif_type="reacts",
                    target_id=target_id,
                    target_type=target_label.lower()
                )
                print("✅ Notification created for unlike.")
            else:
                print("🟡 Skipping notif — user unliked their own post.")
        else:
            print("⚠️ No owner found for target.")

        return {
            "id": record["id"],
            "is_active": record["is_active"],
            "created_at": record["created_at"],
            "user_id": record["user_id"],
            "user_username": record["user_username"],
            "target_id": record["target_id"],
        }










def get_reactors_for_post(post_id: str, current_user: str = None):
    driver = get_driver()
    query = """
    MATCH (p:Post {id: $post_id})
    OPTIONAL MATCH (u:User)-[:REACTED]->(r:React {is_active: true})-[:ON]->(p)
    WITH p, 
         [r IN collect({
             id: r.id,
             type: r.type,
             created_at: r.created_at,
             user_id: u.id,
             user_username: u.username
         }) WHERE r.id IS NOT NULL] AS reacts
    OPTIONAL MATCH (me:User {id: $current_user})-[:REACTED]->(:React {is_active: true})-[:ON]->(p)
    RETURN p.id AS post_id, 
           reacts,
           CASE WHEN me IS NOT NULL THEN true ELSE false END AS has_liked,
           size(reacts) AS like_count
    """
    with driver.session() as session:
        result = session.run(query, post_id=post_id, current_user=current_user)
        record = result.single()
        if not record:
            return None
        return {
            "post_id": record["post_id"],
            "reacts": record["reacts"],
            "has_liked": record["has_liked"],
            "like_count": record["like_count"]
        }
