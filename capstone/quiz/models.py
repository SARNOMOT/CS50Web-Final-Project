from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.

# Define a custom user model inheriting from AbstractUser
class User(AbstractUser):
    pass

# Define choices for difficulty levels
DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard')
)

# Define a Quiz model with various fields
class Quiz(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    topic = models.CharField(max_length=50)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz should finish")
    required_score = models.IntegerField(help_text="required score to pass the exam")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    # Define a method to get questions associated with the quiz
    def get_questions(self):
        return self.question_set.all()

# Define a Question model with text, associated quiz, and creation date
class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    # Define a method to get answers associated with the question
    def get_answers(self):
        return self.answer_set.all()

# Define an Answer model with text, correctness, associated question, and creation date
class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'question: {self.question.text}, answer: {self.text}, correct: {self.correct}'

# Define a Result model with associated quiz, user, score, and pass status    
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    passed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)