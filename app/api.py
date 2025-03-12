from fastapi import FastAPI, Depends
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.model import PostSchema, UserSchema, UserLoginSchema


posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI()

# welcome message
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to your blog!"}

# get all posts
@app.get("/posts", tags=["posts"])
async def get_posts():
    return { "data": posts }

# get single post
@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int):
    if id > len(posts):
        return {"error": "No such post with the supplied ID."}

    for post in posts:
        if post["id"] == id:
            return {"data": post}
        
# add a new post
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(dict(post))
    return {"data": "post added."}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema):
    users.append(user) # replace with db call, making sure to hash the password first
    return sign_jwt(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }


