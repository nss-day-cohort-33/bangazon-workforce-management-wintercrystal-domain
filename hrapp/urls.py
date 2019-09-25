from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name="login"),
    path('computers/', computer_list, name='computer_list'),
    path('computer/form', computer_form, name='computer_form'),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/form', employee_form, name='employee_form'),
    path('trainingprograms/', training_list, name='training_list'),
    # path('trainingprograms/<int:program_id>/', program_details, name='program')
    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('department/<int:department_id>/', department_details, name='department_details'),

]
