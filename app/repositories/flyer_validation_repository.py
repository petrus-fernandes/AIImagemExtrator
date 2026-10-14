class FlyerValidationRepository:

    def __init__(self, session):
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
