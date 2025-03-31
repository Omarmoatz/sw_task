import uuid

from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


class Category(MPTTModel):
    """
    Category Model using MPTT for hierarchical data
    This model allows categories
    to have parent-child relationships with unlimited depth.
    It is useful for representing nested categories in an efficient way.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )  # Self-referencing foreign key to define parent-child hierarchy

    class MPTTMeta:
        order_insertion_by = [
            "name",
        ]  # Ensures categories are ordered alphabetically by name

    def __str__(self):
        return self.name
