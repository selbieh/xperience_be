from modeltranslation.translator import register, TranslationOptions
from .models import Policy

@register(Policy)
class PolicyTranslationOptions(TranslationOptions):
    fields = ('content',)