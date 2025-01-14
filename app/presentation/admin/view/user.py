from sqladmin import ModelView

from presentation.admin.view.init import UserProxy


class UserAdmin(ModelView, model=UserProxy):
    name = "User"
    column_list = ["id", "login", "email", "hashed_password"]
