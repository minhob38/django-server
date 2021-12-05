class Router:
    route_app_labels = ["postgresql"]

    def db_for_read(self, model, **hints):
        print("db for read")
        print(model._meta.app_label)
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label
        return None

    def db_for_write(self, model, **hints):
        print("db for write")
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        print("allow relation")
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print("allow migrate")
        if app_label in self.route_app_labels:
            return app_label
        return None
