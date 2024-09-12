import json
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django import forms
from django.forms import inlineformset_factory

from .models import Result, User, Quiz, Answer, Question
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# Define a view to render the index page with paginated quiz objects
def index(request):
    # Get the list of objects
    object_List = Quiz.objects.all() 
    paginator = Paginator(object_List, 8)  # 8 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'quiz/index.html', {
        'object_List': object_List,
        'page_obj': page_obj
        })

# Define a view to render a specific quiz using its ID
def quiz_view(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    return render(request, 'quiz/quiz.html', {
        'obj': quiz
        })

# Define a view to get quiz data (questions and answers) for a specific quiz using its ID
def get_quiz_data(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
        
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

# Define a function to calculate the score for a quiz
def calculate_score(data, quiz):
    total_questions = quiz.number_of_questions
    correct_answers = 0

    for question in quiz.get_questions():
        question_id = str(question)
        user_answer = data.get(question_id)

        print(f'Question ID: {question_id}, User Answer: {user_answer}')

        if user_answer:
            correct_answer = question.get_answers().filter(correct=True).first()

            if correct_answer and correct_answer.text == user_answer:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100

    print(f'Correct Answers: {correct_answers}, Total Questions: {total_questions}, Score: {score}')

    return score

# Define a function to check if the user passed or failed the quiz
def check_pass_fail(calculated_score, required_score):
    print(f'Calculated Score: {calculated_score}, Required Score: {required_score}')
    result = calculated_score >= required_score
    print(f'Result: {result}')
    return result

# Define a view to save quiz results
@csrf_exempt
def save_quiz(request, quiz_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quiz = Quiz.objects.get(pk=quiz_id)

        calculated_score = calculate_score(data, quiz)
        required_score = quiz.required_score

        passed = check_pass_fail(calculated_score, required_score)
        
        # Check if the user is logged in
        if request.user.is_authenticated:  
            result = Result.objects.create(
                quiz=quiz,
                user=request.user,
                score=calculated_score,
                passed=passed
            )
            result.save()

        return JsonResponse({'message': 'Quiz results saved successfully', 'passed': passed})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Define a view to display quiz results   
def results_view(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)

    results = Result.objects.filter(quiz=quiz).order_by('pk').reverse()

    
    return render(request, 'quiz/results.html', {
        'quiz': quiz,
        'results': results,
        'passed': results.first().passed
    })

# Define a view to filter quizzes by topic
def chosen_topic(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        object_List = Quiz.objects.filter(topic=topic)
        paginator = Paginator(object_List, 8)  # 8 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "quiz/index.html", {
        'object_List': object_List,
        'page_obj': page_obj
    })

# Define a view for user login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("quiz:index"))
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "quiz/login.html")

# Define a view for user logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("quiz:index"))

# Define a view for user registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "quiz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("quiz:index"))
    else:
        return render(request, "quiz/register.html")