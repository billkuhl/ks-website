from web.controllers.account import account as account_blueprint
from web.controllers.admin import admin as admin_blueprint
from web.controllers.default import main as main_blueprint
from web.controllers.error import page_not_found, forbidden
from web.controllers.settings import settings as settings_blueprint
from web import app

# Initialize App blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(account_blueprint, url_prefix='/')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(settings_blueprint, url_prefix='/settings')

# Initialize error handlers
app.register_error_handler(404, page_not_found)
app.register_error_handler(403, forbidden)