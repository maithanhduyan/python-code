# File: core/entities/item.py

from datetime import datetime

class Item:
    def __init__(self, name, code, note=None, created_date=None, updated_date=None):
        self.name = name
        self.code = code
        self.note = note
        self.created_date = created_date or datetime.utcnow()
        self.updated_date = updated_date or datetime.utcnow()

    def update(self, name=None, code=None, note=None):
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code
        if note is not None:
            self.note = note
        self.updated_date = datetime.utcnow()
