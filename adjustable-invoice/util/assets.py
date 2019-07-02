from flask_assets import Bundle, Environment


def register_assets(app):

    bundles = {
        'styles': Bundle(
            'stylesheets/normalize.css',
            'stylesheets/application.scss',
            filters='pyscss',
            output='output/styles.css'
        ),
        'js': Bundle(
            'javascript/application.js',
            output='output/javascript.js'
        )
    }

    assets = Environment(app)
    assets.register(bundles)
