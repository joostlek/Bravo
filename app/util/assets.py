from flask_assets import Bundle, Environment
from .. import app

bundles = {
    'dashboard_js': Bundle(
        'js/lib/material.min.js',
        output='gen/dashboard.js'
    ),

    'dashboard_css': Bundle(
        'css/lib/material.min.css',
        'css/dashboard.css',
        output='gen/dashboard.css'
    )
}

assets = Environment(app)
assets.register(bundles)
