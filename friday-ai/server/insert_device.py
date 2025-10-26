import db_controller
import sys

args = sys.argv

db = db_controller.DatabaseController()
db.add_device(args[1])



