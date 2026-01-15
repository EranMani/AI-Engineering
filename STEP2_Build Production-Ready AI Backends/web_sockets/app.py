import uuid
import json
from fastapi import FastAPI, WebSocket
import redis.asyncio as redis

# establish server
app = FastAPI()

# connect to redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/generate")
async def generate_image(prompt: str):
    # create a unique ID for this job
    job_id = str(uuid.uuid4())

    # bundle the data
    task_data = {
        "id": job_id,
        "prompt": prompt
    }

    # push to the job_queue list in redis
    await redis_client.lpush("job_queue", json.dumps(task_data))

    # return the ID to the user 
    return {"job_id": job_id, "status": "queued"}

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    # user browser knocks on the door. This line is opening and door and makes sure
    # the line is open
    # without this, the browser would try to connect and get rejected immediately
    await websocket.accept()

    # after connection, it grabs the redis radio (pubsub) and tunes to the specific channel
    # without this, the connection would be open but the server would never hear the worker say
    # im done
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(job_id)

    try:
        while True:
            # check for message from redis
            # get_message(ignore_subscribe_messages=True) skips the "you successfully subscribed" validation message
            message = await pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                # redis sends bytes, so we decode it
                data = message["data"].decode("utf-8")

                # forward the data to the users browser
                await websocket.send_text(data)

    except Exception as e:
        # handle disconnection
        print(f"Connection closed: {e}")