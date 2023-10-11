import databases, sqlalchemy, os
from typing import List
from fastapi import FastAPI
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, select

from dotenv import load_dotenv


from .utils import get_questions, already_exists
from .models import QuestionsNum, Question


app: FastAPI = FastAPI()


load_dotenv()

DATABASE_URL: str = os.getenv("DB_URL")

database = databases.Database(DATABASE_URL)

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

engine = sqlalchemy.create_engine(DATABASE_URL)

meta.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/", response_model=Question)
async def questions_request(item: QuestionsNum):
    for item in range(item.questions_num):
        q = get_questions()

        while await already_exists(questions, database, q["original_id"]):
            q = get_questions()

        query = questions.insert().values(
            original_id=q["original_id"],
            question=q["question"],
            answer=q["answer"],
            created_at=q["created_at"],
        )
        last_id = await database.execute(query)
    last_item_query = questions.select().where(questions.c.id == last_id - 1)
    last_question = await database.fetch_one(last_item_query)
    return dict(last_question)


@app.get("/", response_model=List[Question])
async def get_quest():
    query = questions.select()
    return await database.fetch_all(query)
