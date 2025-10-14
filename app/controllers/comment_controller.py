from app.services.neo4j_service import get_driver
import uuid, datetime
from app.controllers.notification_controller import create_notification
def create_comment(user_id: str, post_id: str, content: str):
    driver = get_driver()
    comment_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat()

    query = """
    MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
    CREATE (c:Comment {
        id: $comment_id,
        content: $content,
        created_at: $created_at
    })
    MERGE (u)-[:COMMENTED]->(c)
    MERGE (c)-[:ON]->(p)
    RETURN c AS comment, u AS user, p AS post
    """

    with driver.session() as session:
        record = session.run(
            query,
            user_id=user_id,
            post_id=post_id,
            comment_id=comment_id,
            content=content,
            created_at=created_at
        ).single()

        if not record:
            print("⚠️ No record returned from comment creation.")
            return None

        print("✅ Comment created successfully.")

        # 🔹 Get post owner
        owner_query = """
        MATCH (owner:User)-[:AUTHORED]->(p:Post {id: $post_id})
        RETURN owner.id AS owner_id
        """
        owner_result = session.run(owner_query, {"post_id": post_id}).single()

        if owner_result:
            receiver_id = owner_result["owner_id"]
            if receiver_id != user_id:
                # 🔔 Create notification for post owner
                create_notification(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    message="Commented on your post.",
                    notif_type="comments",
                    target_id=post_id,
                    target_type="post"
                )
                print("✅ Notification created for comment.")
            else:
                print("🟡 Skipping notif — user commented on their own post.")
        else:
            print("⚠️ No post owner found.")

        return {
            "comment": {
                "id": record["comment"]["id"],
                "content": record["comment"]["content"],
                "created_at": record["comment"]["created_at"]
            },
            "user": {
                "id": record["user"]["id"],
                "username": record["user"]["username"]
            },
            "post": {
                "id": record["post"]["id"],
                "content": record["post"]["content"]
            }
        }

def get_comments_for_post(post_id: str):
    driver = get_driver()
    query = """
    MATCH (u:User)-[:COMMENTED]->(c:Comment)-[:ON]->(p:Post {id: $post_id})
    RETURN c, u, p
    ORDER BY c.created_at ASC
    """
    with driver.session() as session:
        result = session.run(query, post_id=post_id)
        return [{"comment": record["c"], "user": record["u"], "post": record["p"]} for record in result]
