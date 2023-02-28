from aiohttp.web_app import Application


def setup_routes(app: Application):
    from admin_api.admin.routes import setup_routes as admin_setup_routes
    from admin_api.quiz.routes import setup_routes as quiz_setup_routes

    admin_setup_routes(app)
    quiz_setup_routes(app)
