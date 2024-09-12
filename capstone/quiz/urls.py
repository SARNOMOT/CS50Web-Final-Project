from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('quiz/<int:quiz_id>', views.quiz_view, name='quiz_view'),
    path('data/<int:quiz_id>', views.get_quiz_data, name='quiz_data_view'),
    path('save/<int:quiz_id>', views.save_quiz, name='save_quiz_view'),
    path('topic', views.chosen_topic, name='topic'),
    path('results/<int:quiz_id>', views.results_view, name='results')
]