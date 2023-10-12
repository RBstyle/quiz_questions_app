import databases, sqlalchemy, os
from typing import List
from fastapi import FastAPI
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, select

from dotenv import load_dotenv


from .utils import get_question, already_exists
from .models import QuestionsNum, Question

load_dotenv()

app: FastAPI = FastAPI(
    title="Quiz questions application",
    version="1.0",
    description="Simple dockerized RESTful app with FastAPI framework",
)

DATABASE_URL: str = os.getenv("DB_URL")
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

meta: MetaData = MetaData()

questions: Table = Table(
    "questions",
    meta,
    Column("id", Integer, primary_key=True),
    Column("original_id", Integer),
    Column("question", String),
    Column("answer", String),
    Column("created_at", DateTime),
)


meta.create_all(engine)


@app.on_event("startup")
async def startup():
    """Establishes a connection pool before the application starts"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Closes all connections in the connection pool
    when the application is shutting down"""
    await database.disconnect()


@app.post("/", response_model=Question | dict, tags=["Questions"])
async def questions_request(questions_num: QuestionsNum):
    """Receive questions from a third party API:

    Args:
        questions_num (QuestionsNum): Number of questions.
            QuestionsNum object instance(i.e. {"questions_num": integer}).
    Returns:
        Question | dict: Previos question or empty object.
    """
    last_id: int = int()

    # Receive questions and check for availability
    for item in range(questions_num.questions_num):
        q = get_question()

        # Receive another question if current is exists
        while await already_exists(questions, database, q["original_id"]):
            q = get_question()

        # Preparing query to save object
        query = questions.insert().values(
            original_id=q["original_id"],
            question=q["question"],
            answer=q["answer"],
            created_at=q["created_at"],
        )

        # making a request and getting the instance ID
        last_id = await database.execute(query)

    previos_id: int = last_id - 1

    # Return the previous question or an empty object
    if previos_id > 0:
        last_item_query = questions.select().where(questions.c.id == previos_id)
        last_question = await database.fetch_one(last_item_query)
        return Question(**last_question)
    return {}


@app.get("/", response_model=List[Question], tags=["Questions"])
async def get_questions():
    """Get all available questions"""
    query = questions.select()
    return await database.fetch_all(query)
