from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
import uuid
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

origins=["http://localhost:3000",
         "https://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db=[{"username":"username","password":"password"}]

@app.get("/login")

def login(username:str,password:str):
    for user in db:
        if user["username"]==username and pwd_context.verify(password, user["password"]):
            return{"messagae":"you have logged in successfully"}
    print("error")
    print(db)
    print(username,password)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="passwords do not match")



class New_user(BaseModel):
    username:str
    password:str
    password2:str



@app.post("/signup")

def signup(credentials:New_user):
    print(credentials.username)
    print(credentials.password)
    id= str(uuid.uuid4())
    user={"id":id,"username":credentials.username,"password":pwd_context.hash(credentials.password)}

    if credentials.password==credentials.password2:
        db.append(user)
        print(db)
        print(credentials.password)
        print(credentials.username)
        return{"great, you have signed up"}

    else:
        print(credentials.password)
        print(credentials.username)
        print("error")
        print(db)
        raise HTTPException(status_code=405, detail="item")




# class bookings(BaseModel):
#     date:str
#     people:int
#     name:str


# @app.post("booking")

# def booking(info:bookings):
    