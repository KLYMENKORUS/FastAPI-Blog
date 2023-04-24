import uvicorn
from fastapi import FastAPI, APIRouter
from api.actions.users.handlers import user_route
from api.actions.posts.handlers import post_route
from api.actions.comments.handlers import comment_router
from api.actions.authenticate.login_handlers import login_router


app = FastAPI()

# create the instance for the routes
main_api_route = APIRouter()

# set routes to the app instance
main_api_route.include_router(user_route, prefix='/users', tags=['users'])
main_api_route.include_router(post_route, prefix='/post', tags=['post'])
main_api_route.include_router(login_router, prefix='/login', tags=['login'])
main_api_route.include_router(comment_router, prefix='/comment', tags=['comment'])
app.include_router(main_api_route)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)