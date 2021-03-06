from django.db import models
from .employee import Employee
from .computer import Computer

class EmployeeComputer(models.Model):
    """
    Creates the join table for the many to many relationship between computers and employees
    Author: Joe Shep
    methods: none
    """

    employee_id = models.ForeignKey("Employee", on_delete=models.CASCADE)
    computer_id = models.ForeignKey("Computer", on_delete=models.CASCADE)
    assigned_date = models.DateField(default="0000-00-00")
    unassigned_date = models.DateField(null=True, blank=True, default="0000-00-00")
