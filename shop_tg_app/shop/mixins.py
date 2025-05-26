from django.conf import settings
from .models import Category


# добавляет базовый контекст для каждой страницы с layout 
class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # получаем древо дерева из базы данных
        categories = Category.objects.filter(parent=None)
        
        # Общие переменные для шаблонов
        context.update({
            "media_url": settings.MEDIA_URL,
            "base_url": self.request.get_host(),
            "show_sort_bar": False,  # сортировка по умолчанию не отображается
            "show_home_button": False, # кнопка "на главную" по умолчанию есть 
            "categories": categories,
            "tg_username": settings.TG_USERNAME,
            "max_search_characters": settings.MAX_SEARCH_CHARACTERS,
            "min_search_characters": settings.MIN_SEARCH_CHARACTERS,
        })

        return context
