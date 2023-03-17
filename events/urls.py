from django.urls import path

from events import views

urlpatterns = [
    path("", views.ListEventView.as_view()),
    path("<int:pk>/", views.RetriveEventView.as_view()),
    path("create/", views.CreateEventView.as_view()),
    path("update/<int:pk>", views.UpdateEventView.as_view()),
    path("performance/", views.PerformenceView.as_view()),
    path("export/", views.ExportEventsView.as_view()),
    path("performance/manage/", views.ManagePerformeceView.as_view()),
]
