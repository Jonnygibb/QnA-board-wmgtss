from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    """
    Generates a base user class utilising Django built in authorisation module
    """
    pass


class Questions(models.Model):
    """
    Object representing a question posted on the Q&A Board
    """
    # The user foreign key links the logged in user to the selected question
    # instance. By using on delete cascade, a question will be deleted if the
    # user is deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user')
    # Question title field has a unique constraint as questions must be
    # unique in order for them to be slugified and uniquely identified.
    title = models.CharField(max_length=256, unique=True)
    # Using the keyword argument auto_now and auto_now_add automatically
    # updates these two fields when an object is created or when it is updated.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    # A slug field is used to store a unique string which is a concatenated
    # version of the question title. This is used in the url to enable
    # the url itself to reference a question object.
    # Example: localhost:8000/question/this-is-my-first-question
    slug = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        """
        Overwrites the Django object save method
        """
        # On save of object, create the slug based on the object title.
        self.slug = slugify(self.title)
        super(Questions, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Overwites the Django get_absolute_url method for question object
        """
        # Specifies the url of the object detail page. Keyword arguement of
        # slug is used to identify each instance of question object.
        return reverse('question-detail', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Overwrites the Django __str__ method
        """
        # Instructs Django to use the objects title when displaying the
        # instance rather than its location in memory.
        return self.title

    class Meta:
        """
        Associated metadata relevent to the Question object  
        """
        # Orders question instances by earliest creation date by default.
        ordering = ['created_at']


class Answer(models.Model):
    """
    Object representing an answer on the Q&A Board
    """
    # This foreign key field creates a one to one relationship with a question.
    # On delete cascase is also used here as an answer cannot exist without its
    # associated question.
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,
                                 related_name='answer')
    # The user foreign key links the logged in user to the selected answer
    # instance. By using on delete cascade, an answer will be deleted if the
    # user is deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # Using the keyword argument auto_now and auto_now_add automatically
    # updates these two fields when an object is created or when it is updated.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        """
        Associated metadata relevent to the Answer object
        """
        # Orders answer instances by earliest creation date by default
        ordering = ['created_at']


class Comment(models.Model):
    """
    Object representing a comment on the Q&A Board
    """
    # This foreign key field creates a one to one relationship with a question.
    # On delete cascase is also used here as a comment cannot exist without its
    # associated question.
    question = models.ForeignKey(Questions,
                                 on_delete=models.CASCADE,
                                 related_name='comment')
    # The user foreign key links the logged in user to the selected comment instance.
    # By using on delete cascade, a comment will be deleted if the user is deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Using the keyword argument auto_now and auto_now_add automatically updates
    # these two fields when an object is created or when it is updated.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        """
        Associated metadata relevent to the Comment object
        """
        # Orders comment instances by earliest creation date by default
        ordering = ['created_at']
