from app.services.neo4j_service import run_query

def create_or_update_bio(
    user_id: str,
    birthday: str = None,
    status: str = None,
    about: str = None,
    hobbies: str = None,
    skills: str = None,
    interest_tags: str = None,
    school: str = None
):
    query = """
  MATCH (u:User {id: $user_id})
OPTIONAL MATCH (u)-[r:HAS_BIO]->(old:Bio)
DELETE r, old
WITH u
CREATE (newBio:Bio {
    id: randomUUID(),
    birthday: $birthday,
    status: $status,
    about: $about,
    hobbies: $hobbies,
    skills: $skills,
    interest_tags: $interest_tags,
    school: $school
})
CREATE (u)-[:HAS_BIO]->(newBio)
RETURN newBio AS b, u

    """
    result = run_query(query, {
        "user_id": user_id,
        "birthday": birthday,
        "status": status,
        "about": about,
        "hobbies": hobbies,
        "skills": skills,
        "interest_tags": interest_tags,
        "school": school
    }, single=True)

    if not result:
        return None

    return {
        "user_id": result["u"]["id"],
        "bio": {
            "id": result["b"]["id"],
            "birthday": result["b"].get("birthday"),
            "status": result["b"].get("status"),
            "about": result["b"].get("about"),
            "hobbies": result["b"].get("hobbies"),
            "skills": result["b"].get("skills"),
            "interest_tags": result["b"].get("interest_tags"),
            "school": result["b"].get("school"),
        }
    }
