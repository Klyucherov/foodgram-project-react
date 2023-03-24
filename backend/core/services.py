"""Модуль вспомогательных функций.
"""
from django.db import transaction

from recipes.models import AmountIngredient, Recipe


def recipe_amount_ingredients_set(recipe: Recipe,
                                  ingredients: list[dict]) -> None:
    amount_ingredients = []

    for ingredient in ingredients:
        amount_ingredient, created = AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )
        if created:
            amount_ingredients.append(amount_ingredient)

    with transaction.atomic():
        AmountIngredient.objects.bulk_create(amount_ingredients)


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
