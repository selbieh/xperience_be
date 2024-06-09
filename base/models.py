from django.db import models

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Policy(models.Model):
    POLICY_TYPES = (
        ('privacy', 'Privacy Policy'),
        ('terms', 'Terms of Use'),
        ('cancellation', 'Cancellation Policy'),
    )

    key = models.CharField(max_length=20, choices=POLICY_TYPES, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.get_key_display()
    

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()