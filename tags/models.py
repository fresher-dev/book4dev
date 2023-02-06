from django.db import models


class Tag(models.Model):
    """
    Tag model
    -> name
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
