from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(Rules)
class RulesTranslationOptions(TranslationOptions):
    fields = ('rules_name',)
