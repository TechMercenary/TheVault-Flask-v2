# Setting essential environment variables

import os
from config import load_settings
load_settings(root_app_dir=os.path.dirname(__file__))

# Rest of the app

from models import db
from . import app
from populate import populate_first_time

from routes.index import *
from routes.app_settings import *
from routes.currency import *
from routes.holiday import *
from routes.employer import *
from routes.salary_agreement import *
from routes.salary_earned import *
from routes.paycheck import *


def rebuild_db():
    with app.app_context():
        with db.engine.connect() as con:
            for table in reversed(db.metadata.sorted_tables):
                con.exec_driver_sql(f"DROP TABLE IF EXISTS {str(table)} CASCADE;")
            con.commit()
        db.create_all()
        populate_first_time()


if __name__ == '__main__':
    db.init_app(app)
    rebuild_db()
    app.run()
