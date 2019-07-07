from flask import url_for

def register_filters(app):

    @app.template_filter()
    def image_url(path):
        return url_for('static', filename=f"images/{path}")

    @app.template_filter()
    def as_currency(number):
        if number >= 0:
            return '${:0,.2f}'.format(number)
        else:
            return '-${:0,.2f}'.format(-number)
