from filebot.models import File, Category
from typing import Optional, List


def get_parent_categories() -> List[Category]:
    return Category.objects.filter(level=0)


def get_category_by_name(name: str, parent_category: Category = None) -> Optional[Category]:
    if not parent_category:
        return Category.objects.filter(name=name, level=0).first()
    else:
        return parent_category.get_children().filter(name=name)


