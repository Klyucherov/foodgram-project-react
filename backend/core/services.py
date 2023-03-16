"""Модуль вспомогательных функций.
"""
from recipes.models import AmountIngredient, Recipe


def recipe_amount_ingredients_set(
        recipe: Recipe,
        ingredients: list[dict]
) -> None:
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
