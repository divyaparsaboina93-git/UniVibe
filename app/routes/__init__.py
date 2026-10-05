def register_blueprints(app):
    from app.routes.auth import bp as auth_bp
    from app.routes.users import bp as users_bp
    from app.routes.posts import bp as posts_bp
    from app.routes.comments import bp as comments_bp
    from app.routes.follows import bp as follows_bp
    from app.routes.search import bp as search_bp
    from app.routes.notifications import bp as notifications_bp
    from app.routes.messages import bp as messages_bp
    from app.routes.communities import bp as communities_bp
    from app.routes.study_resources import bp as study_resources_bp
    from app.routes.events import bp as events_bp
    from app.routes.reports import bp as reports_bp
    from app.routes.blocks import bp as blocks_bp
    from app.routes.admin import bp as admin_bp

    for bp in (
        auth_bp, users_bp, posts_bp, comments_bp, follows_bp, search_bp,
        notifications_bp, messages_bp, communities_bp, study_resources_bp,
        events_bp, reports_bp, blocks_bp, admin_bp,
    ):
        app.register_blueprint(bp)
