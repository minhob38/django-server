class Router:
    """
    - None이면 settings.py DATABASES의 default database로 연결
    - model에서 app_label정의하지 않으면, app_label은 app의 이름으로 할당
    """
    route_app_labels = ["default", "postgresql"]

    def db_for_read(self, model, **hints):
        # print("db for read")
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label
        return None

    def db_for_write(self, model, **hints):
        # print("db for write")
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # print("allow relation")
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print("allow migrate")
        if app_label in self.route_app_labels:
            return app_label
        return None
