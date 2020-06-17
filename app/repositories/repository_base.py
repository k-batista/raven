class RepositoryBase:
    def __init__(self, app, db):
        self.app = app
        self.db = db

    def session(self):
        return self.db.session

    def create(self, entity):
        with self.app.app_context():
            self.session().add(entity)
            self.session().commit()
            self.session().refresh(entity)
        return entity

    def update(self, entity):
        with self.app.app_context():
            entity = self.session().merge(entity)
            self.session().commit()
            self.session().refresh(entity)
        return entity
