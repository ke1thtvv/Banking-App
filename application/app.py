from flask import Flask, render_template
from datetime import datetime
from .config.config import config, loginManeger
from .models.models import db, create_initial_data, User, Transfer
from .blueprints.auth import auth
from .blueprints.account import account
from .blueprints.transactions import transaction
from .blueprints.transfer import transfer
from .schedule.schechuled_tasks import process_transfer
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)
config(app=app, db = db)

login_manager = loginManeger(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.register_blueprint(auth)
app.register_blueprint(account)
app.register_blueprint(transaction)
app.register_blueprint(transfer)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def process_transfer_queue():
    with app.app_context():
                
        tasks = Transfer.query.filter_by(status = 'waiting').all()      
        for task in tasks:
          process_transfer(task)


with app.app_context():
  db.create_all()
  create_initial_data()
  scheduler = BackgroundScheduler()
  scheduler.add_job(func=process_transfer_queue, trigger='cron', minute='0/15', hour='10-23')
  scheduler.start()




if __name__ == '__main__':   
    with app.app_context():
        db.create_all()
        app.run(debug=True)