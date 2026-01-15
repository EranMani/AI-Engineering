from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import models, schemas
from database import engine, get_db, Base

# lifecycle manager
# Since we can't run sync code like 'Base.metadata.create_all' directly,
# we use a lifespan context manager.
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown : (optional cleanup)

app = FastAPI(lifespan=lifespan)

@app.post("/votes", response_model=schemas.VoteResponse)
async def cast_vote(vote: schemas.VoteCreate, db: AsyncSession = Depends(get_db)):
    # create object
    new_vote = models.VoteDB(candidate_name=vote.candidate_name)

    # add to session
    db.add(new_vote)

    # commit (must await!)
    await db.commit()

    # refresh (must await!)
    await db.refresh(new_vote)

    return {"id": new_vote.id, "candidate_name": new_vote.candidate_name, "message": "Vote cast!"}

@app.get("/results/")
async def get_results(db: AsyncSession = Depends(get_db)):
    # sql :
    # SELECT candidate_name, COUNT(*) FROM votes GROUP BY candidate_name
    stmt = (
        select(models.VoteDB.candidate_name, func.count(models.VoteDB.id))
        .group_by(models.VoteDB.candidate_name)
    )

    # execute (must await!)
    result = await db.execute(stmt)

    # process data. all gives a list of rows
    votes = result.all()

    # convert to a clean json format
    return [{"candidate": row[0], "count": row[1]} for row in votes]