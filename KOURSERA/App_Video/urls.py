from django.urls import path
from . import views

app_name = "App_Video"

urlpatterns = [
    path('courses/',views.get_courses_for_user,name="courses"),
    path('stream/<slug>',views.course_stream,name="stream")
]
