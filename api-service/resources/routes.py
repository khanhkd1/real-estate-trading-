from .post import PostsApi


def initialize_routes(api):
    api.add_resource(PostsApi, '/posts')
