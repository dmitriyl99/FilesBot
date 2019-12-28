from filebot.models import File, Category
from typing import Optional, List


def get_parent_categories() -> List[Category]:
    return Category.objects.filter(level=0)


def get_category_by_name(name: str, parent_category: Category = None) -> Optional[Category]:
    if not parent_category:
        return Category.objects.filter(name=name, level=0).first()
    else:
        return parent_category.get_children().filter(name=name).first()


def get_file_by_id(file_id: int) -> Optional[File]:
    try:
        return File.objects.get(pk=file_id)
    except File.DoesNotExist:
        return None


def get_file_by_name(file_name: str) -> Optional[File]:
    return File.objects.filter(name=file_name).first()


def get_users_files() -> List[File]:
    return File.objects.filter(is_user_file=True, confirmed=True)


def search_files(query: str) -> List[File]:
    # TODO: Fix this part of code when migrate to other database. Case-insensitive doesn't work in SQLite
    all_files = File.objects.filter(confirmed=True)
    result = []
    query = query.upper()
    for file in all_files:
        if query in file.name.upper():
            result.append(file)
    return result
