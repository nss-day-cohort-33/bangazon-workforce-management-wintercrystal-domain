from django.db import models
from .employee import Employee
from .training import Training

class EmployeeComputer(models.Model):
    """
    Creates the join table for the many to many relationship between computers and employees
    Author: Joe Shep
    methods: none
    """

    employee_id = models.ForeignKey("Employee", on_delete=models.CASCADE)
    training_id = models.ForeignKey("Training", on_delete=models.CASCADE)
