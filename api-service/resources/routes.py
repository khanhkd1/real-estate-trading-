from .post import PostsApi
from .auth import SignupApi, LoginApi
from .user import UserApi


def initialize_routes(api):
    api.add_resource(PostsApi, '/api/posts')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(UserApi, '/api/user')
