def get_recipes_count_label(count: int) -> str:
    if count > 1:
        return f"{count} ingredients"
    elif count == 1:
        return f"1 ingredient"
    else:
        return "No ingredients"