"""Модуль валидаторов.
"""
from re import compile
from string import hexdigits
from typing import Dict, List, Optional, TYPE_CHECKING, Union

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

if TYPE_CHECKING:
    from recipes.models import Ingredient, Tag


@deconstructible
class OneOfTwoValidator:
    first_regex = '[^а-яёА-ЯЁ]+'
    second_regex = '[^a-zA-Z]+'
    field = 'Переданное значение'
    message = '<%s> на разных языках либо содержит не только буквы.'

    def __init__(
            self,
            first_regex: Optional[Union[str, None]] = None,
            second_regex: Optional[Union[str, None]] = None,
            field: Optional[Union[str, None]] = None,
    ) -> None:
        if first_regex is not None:
            self.first_regex = first_regex
        if second_regex is not None:
            self.second_regex = second_regex
        if field is not None:
            self.field = field
        self.message = f'\n{self.field} {self.message}\n'

        self.first_regex = compile(self.first_regex)
        self.second_regex = compile(self.second_regex)

    def __call__(self, value: str) -> None:
        if self.first_regex.search(value) and self.second_regex.search(value):
            raise ValidationError(self.message % value)


@deconstructible
class MinLenValidator:
    min_len = 0
    field = 'Переданное значение'
    message = '\n%s недостаточной длины.\n'

    def __init__(
            self,
            min_len: Optional[Union[int, None]] = None,
            field: Optional[Union[str, None]] = None,
            message: Optional[Union[str, None]] = None,
    ) -> None:
        if min_len is not None:
            self.min_len = min_len
        if field is not None:
            self.field = field
        if message is not None:
            self.message = message
        else:
            self.message = self.message % field

    def __call__(self, value: int) -> None:
        if len(value) < self.min_len:
            raise ValidationError(self.message)


def hex_color_validator(color: str) -> str:
    color = color.strip(' #')
    if len(color) not in (3, 6):
        raise ValidationError(
            f'Код цвета {color} не правильной длины ({len(color)}).'
        )
    if not set(color).issubset(hexdigits):
        raise ValidationError(
            f'{color} не шестнадцатиричное.'
        )
    if len(color) == 3:
        return f'#{color[0] * 2}{color[1] * 2}{color[2] * 2}'.upper()
    return '#' + color.upper()


def tags_exist_validator(tags_ids: List[Union[int, str]], Tag: 'Tag') -> None:
    exists_tags = Tag.objects.filter(id__in=tags_ids)

    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_exist_validator(
        ingredients: List[Dict[str, Union[str, int]]],
        Ingredient: 'Ingredient'
) -> List[Dict[str, Union[int, 'Ingredient']]]:
    ings_ids = [None] * len(ingredients)

    for idx, ing in enumerate(ingredients):
        ingredients[idx]['amount'] = int(ingredients[idx]['amount'])
        if ingredients[idx]['amount'] < 1:
            raise ValidationError('Неправильное количество ингидиента')
        ings_ids[idx] = ing.pop('id', 0)

    ings_in_db = Ingredient.objects.filter(id__in=ings_ids).order_by('pk')
    ings_ids.sort()

    for idx, id in enumerate(ings_ids):
        ingredient: 'Ingredient' = ings_in_db[idx]
        if ingredient.id != id:
            raise ValidationError('Ингридент не существует')

        ingredients[idx]['ingredient'] = ingredient
    return ingredients
