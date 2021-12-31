from .post import PostsApi, PostApi, PostsUserApi, PredictPrice
from .auth import SignupApi, LoginApi
from .user import UserApi
from .reset_password import ForgotPassword, ResetPassword
from .image import ImageApi
from .follow import FollowApi, FollowsApi
from .admin.auth import AdminLoginApi
from .admin.dashboard import DashBoard
from .admin.user import AdminUsersApi, AdminUserApi


def initialize_routes_api(api):
    # admin
    api.add_resource(AdminLoginApi, '/api/admin/login')
    api.add_resource(DashBoard, '/api/admin/dashboard')
    api.add_resource(AdminUsersApi, '/api/admin/user')
    api.add_resource(AdminUserApi, '/api/admin/user/<int:user_id>')

    api.add_resource(PostsApi, '/api/posts')
    api.add_resource(PostApi, '/api/post/<int:post_id>')
    api.add_resource(PostsUserApi, '/api/posts/user')
    api.add_resource(PredictPrice, '/api/posts/predict')

    api.add_resource(FollowsApi, '/api/posts/follow')
    api.add_resource(FollowApi, '/api/post/follow/<int:post_id>')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/reset/<string:reset_token>')

    api.add_resource(UserApi, '/api/user')

    api.add_resource(ImageApi, '/api/image')
