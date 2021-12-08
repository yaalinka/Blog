from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('profile/', Profile.as_view(), name='profile'),
    path('edit_article/<slug:article_slug>/', EditArticle.as_view(), name='edit_article'),
    path('article/<slug:article_slug>/', ReadArticle.as_view(), name='article'),
    path('delete_article/<slug:article_slug>/', DeleteArticle.as_view(), name='delete_article'),
    path('chosen_category/<int:pk>/', ChosenCategory, name='chosen_category'),
]