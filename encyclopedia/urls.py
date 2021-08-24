from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit_Entry, name="edit_Entry"),
    path("wiki/<str:title>/submit", views.submit_Edit_Entry, name="submit_Edit_Entry"),
    path("wiki/", views.randomEntry, name="randomEntry"),
     path("delete/<str:title>", views.deleteEntry, name="delete"),
    
]
