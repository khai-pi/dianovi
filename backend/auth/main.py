import os

import httpx
import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Auth works also as API Gateway

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all, but be careful with that in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = os.getenv("JWT_SECRET", "supersecretkey")
PATIENT_SERVICE_URL = os.getenv("PATIENT_SERVICE_URL", "http://patient:8000")
RECOMMENDATION_SERVICE_URL = os.getenv(
    "RECOMMENDATION_SERVICE_URL", "http://recommendation:8000"
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/login")
def login(req: LoginRequest):
    # Mockup
    # TODO Implement real authentication, encrypt password in database
    if req.username == "doctor" and req.password == "password":
        token = jwt.encode({"sub": req.username}, SECRET, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# Forward requests to the patient service
@app.api_route(
    "/api/patients{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"]
)
async def proxy_patients(request: Request, full_path: str):
    return await forward_request(
        request=request,
        target_base_url=PATIENT_SERVICE_URL,
        forward_path=f"/patients{full_path}",
        protected=True,
    )


# Forward requests to the recommendation service
@app.api_route(
    "/api/recommend{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"]
)
async def proxy_recommend(request: Request, full_path: str):
    return await forward_request(
        request=request,
        target_base_url=RECOMMENDATION_SERVICE_URL,
        forward_path=f"/recommend{full_path}",
        protected=True,
    )


async def forward_request(
    request: Request, target_base_url: str, forward_path: str, protected: bool = False
):
    # Check auth if required
    if protected:
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        try:
            jwt.decode(auth.replace("Bearer ", ""), SECRET, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    # Prepare the forwarded request
    async with httpx.AsyncClient() as client:
        url = f"{target_base_url}{forward_path}"
        method = request.method
        headers = dict(request.headers)
        body = await request.body()

        # Forward the request
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body,
        )
        return JSONResponse(status_code=response.status_code, content=response.json())
