from flask import url_for


def register_filters(app):

    @app.template_filter()
    def image_url(path):
        return url_for('static', filename=f"images/{path}")
