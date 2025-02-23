from django.urls import path
from . import views
urlpatterns = [
    path('',views.search,name="search"),
    path("sm/",views.sm),
    path("search_suggestions/",views.ingridient_search_sugguestions,name="search_suggestions"),
    path("fetch_recipes/",views.fetch_recipes,name="fetch_recipes"),
    path("recipe_details/<int:id>",views.recipe_details,name="recipe_details"),
]