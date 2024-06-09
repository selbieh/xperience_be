from modeltranslation.translator import register, TranslationOptions
from .models import CarMake, HotelService

@register(HotelService)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(CarMake)
class CarMakeTranslationOptions(TranslationOptions):
    fields = ('name',)

