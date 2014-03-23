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


class override_settings(object):
    tmp_settings = {}

    def __init__(self, **settings):
        self.override_settings = settings

    def __enter__(self):
        from foomn import get_settings, set_settings
        self.tmp_settings = get_settings()
        settings = get_settings()
        settings.update(self.override_settings)
        set_settings(settings)
        return self

    def __exit__(self, *args):
        from foomn import set_settings
        set_settings(self.tmp_settings)

    def __call__(self, func):
        from functools import wraps

        @wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapped
