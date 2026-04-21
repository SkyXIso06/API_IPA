import mysql.connector as mc
from configdb import DB_CFG

class Database:
    def __init__(self, cfg=None):
        self.cfg=cfg or DB_CFG

    def connect(self):
        return mc.connect(**self.cfg)