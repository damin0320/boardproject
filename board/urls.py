from django.urls import path
from .views import CreateBoardView, ReadBoardView, UpdateBoardView, DeleteBoardView

urlpatterns = [
    path('', CreateBoardView.as_view()),
    path('/read', ReadBoardView.as_view()),
    path('/edit', UpdateBoardView.as_view()),
    path('/delete', DeleteBoardView.as_view())

]