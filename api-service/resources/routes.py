from .post import PostsApi, PostApi, PostsUserApi
from .auth import SignupApi, LoginApi
from .user import UserApi
from .reset_password import ForgotPassword, ResetPassword
from .image import ImageApi


def initialize_routes_api(api):
    api.add_resource(PostsApi, '/api/posts')
    api.add_resource(PostApi, '/api/post/<int:post_id>')
    api.add_resource(PostsUserApi, '/api/posts/user')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/reset/<string:reset_token>')

    api.add_resource(UserApi, '/api/user')

    api.add_resource(ImageApi, '/api/image')
