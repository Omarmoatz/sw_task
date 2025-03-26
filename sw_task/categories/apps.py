import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesConfig(AppConfig):
    name = "sw_task.categories"
    verbose_name = _("Categories")

    def ready(self):
        with contextlib.suppress(ImportError):
            import sw_task.categories.signals  # noqa: F401
