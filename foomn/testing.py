def setup_models():
    from sqlalchemy import create_engine
    from foomn import models
    engine = create_engine("sqlite:///")
    models.Base.metadata.create_all(bind=engine)
    models.DBSession.remove()
    models.DBSession.configure(bind=engine)
    return models


def teardown_models():
    import transaction
    transaction.abort()
    from foomn import models
    models.DBSession.remove()
