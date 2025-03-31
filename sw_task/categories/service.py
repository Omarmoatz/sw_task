import uuid

from sw_task.categories.exceptions import CategoryNotFoundError
from sw_task.categories.models import Category


class CategoriesService:
    """
    Service Layer for handling Category operations
    This service class abstracts database operations, keeping views and models clean.
    """

    model = Category

    def get_model(self) -> Category:
        """Return the model associated with this service."""
        return self.model

    def create_initial_categories(self) -> list[Category]:
        """Create initial categories if none exist."""
        model = self.get_model()
        if not model.objects.exists():
            initial_categories = ["Category A", "Category B"]
            for name in initial_categories:
                model.objects.create(name=name)

    def create_categories(self, validated_data: list[dict]) -> list[Category]:
        """Create multiple categories while avoiding duplicates."""
        categories = []
        model = self.get_model()
        for item in validated_data:
            # If category with this name already exists, skip it
            if model.objects.filter(name=item["name"]).exists():
                continue
            category = model.objects.create(**item)
            categories.append(category)
        return categories

    def get_category(self, category_id: uuid.UUID) -> Category:
        """Retrieve a specific category by ID, or raise an error if not found."""
        model = self.get_model()
        try:
            return model.objects.get(id=category_id)
        except model.DoesNotExist:
            raise CategoryNotFoundError from None

    def get_categories(self) -> list[Category]:
        """Retrieve all root categories (categories with no parent)."""
        model = self.get_model()
        return model.objects.filter(parent=None)
    
    def get_all_sub_categories(self) -> list[Category]:
        """Retrieve all root sub categories (categories with any parent)."""
        model = self.get_model()
        return model.objects.filter(parent__isnull=False)

    def create_subcategories(
        self,
        parent_id: uuid.UUID,
    ) -> list[Category]:
        """
        Create subcategories for a given parent category while avoiding duplicates.
        """
        parent = self.get_category(parent_id)
        model = self.get_model()

        subcategories = []
        subcategory_names = [
            f"SUB {parent.name}-1",
            f"SUB {parent.name}-2",
        ]
        for name in subcategory_names:
            # If subcategory with this name already exists, change the name
            if model.objects.filter(name=name).exists():
                name = f"SUB {name}"

            subcategory = model.objects.create(parent=parent, name=name)
            subcategories.append(subcategory)
        return subcategories

    def get_subcategories(
        self,
        parent_id: uuid.UUID,
        values: tuple[str],
    ) -> list[Category] | list[dict]:
        """
        Retrieve subcategories for a given parent category,
        with optional filtering.
        """
        parent = self.get_category(parent_id)
        if values:
            return list(parent.get_children().values(*values))  # Fetch specific fields
        return parent.get_children()

    def create_category_name(self, parent_name: str, subcategory_number: int) -> str:
        """Generate a unique name for subcategories based on parent name and index."""
        prefix = "SUB "
        return f"{prefix}{parent_name}-{subcategory_number + 1}"

    def create_subcategory_names(self, parent_name: str, count: int) -> list[str]:
        """Generate a list of subcategory names dynamically."""
        return [
            self.create_category_name(parent_name, i - 1) for i in range(1, count + 1)
        ]

    def get_or_create_subcategories(
        self,
        parent_id: uuid.UUID,
        validated_data: list[dict] | None = None,
        values: tuple[str] | None = None,
    ) -> list[Category]:
        """
        Retrieve subcategories for a parent or create them if none exist.
        """
        subcategories = self.get_subcategories(parent_id, values)
        if len(subcategories) == 0:
            if not validated_data:
                validated_data = [
                    {"name": name}
                    for name in self.create_subcategory_names(
                        self.get_category(parent_id).name,
                        2,
                    )
                ]
            subcategories = self.create_subcategories(parent_id, validated_data)
            return self.get_subcategories(parent_id, values)
        return subcategories

    def delete_all_subcategories(self):
        """delete all the sub categories"""
        categories = self.get_all_sub_categories()
        for ctg in categories:
            ctg.delete()
