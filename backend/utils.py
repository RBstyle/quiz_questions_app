import requests
from fastapi.exceptions import HTTPException
from dateutil import parser


def get_questions() -> dict | None:
    try:
        r = requests.get("https://jservice.io/api/random")
        r.raise_for_status()
    except:
        raise HTTPException(status_code=429, detail="Too many requests")
    response_data = r.json()[0]
    created_datetime = parser.parse(response_data.get("created_at")).replace(
        tzinfo=None
    )
    data: dict = {
        "original_id": response_data.get("id"),
        "question": response_data.get("question"),
        "answer": response_data.get("answer"),
        "created_at": created_datetime,
    }
    return data


async def already_exists(questions, database, id) -> bool:
    query = questions.select().where(questions.c.original_id == id)
    res = await database.fetch_one(query)
    return False if not res else True
