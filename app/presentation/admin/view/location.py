from sqladmin import ModelView

from presentation.admin.view.init import LocationProxy


class LocationAdmin(ModelView, model=LocationProxy):
    name = "Location"
    column_list = ["id", "name", "user_id", "latitude", "longitude"]
