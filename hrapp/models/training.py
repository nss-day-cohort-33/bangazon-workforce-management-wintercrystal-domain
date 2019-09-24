from django.db import models
from .department import Department

class Training(models.Model):

    title = models.CharField(max_length=55)
    start_date = models.DateField(default="0000-00-00")
    end_date = models.DateField(default="0000-00-00")
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("Training_detail", kwargs={"pk": self.pk})
