from django.db import models
import uuid
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.validators import RegexValidator
# Create your models here.

class Employee(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    Emp_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50,default="gmail.com")
    
    
    contract_no = models.IntegerField()
    s_no = models.IntegerField()
    #state = models.CharField(max_length=30,default='000000')
    state = models.CharField(
        max_length=100,
        default='',
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                #message='Only alphabetic characters are allowed for the state field.',
                code='invalid_state'
            )
        ]
    )
    
    programme = models.CharField(
        max_length=100,
        default='',
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                code='invalid_state'
            )
        ]
    )
    
    designation=models.CharField(max_length=100,default = "",null=True)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    profFee_monthly = models.CharField(max_length=50,default = "",null=True)
    P_F_Budget = models.DecimalField(max_digits=12, decimal_places=2,default=0.00) #Wrong
    #Done
    Travel_Budget = models.DecimalField(max_digits=20, decimal_places=2,default=0.00)
    Travel_Days_Budget= models.DecimalField(max_digits=20, decimal_places=2,default=0.00)
    DSA_Budget = models.DecimalField(max_digits=20, decimal_places=2,default=0.00)
    DSA_Days_Budget = models.DecimalField(max_digits=20, decimal_places=2,default=0.00)
    Terminal_Charges_Budget = models.DecimalField(max_digits=5, decimal_places=2, blank=True,default=0.00)

    def __str__(self):
        return str(self.Emp_name)

def get_upload_path(instance,filename):
    return os.path.join('Advance Trip Plans/' +  str(instance.employee.Emp_name),filename)

class AdvancedTravelPlan(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    month = models.CharField(choices = [
        ('January', 'January'),
        ('February', 'February'),
        ('March' , 'March'),
        ('April','April'),
        ('May','May'),
        ('June','June'),
        ('July','July'),
        ('August','August'),
        ('September','September'),
        ('October','October'),
        ('November','November'),
        ('December','December')
    ],default = "January",max_length=10)
    year = models.CharField(max_length=20,default = "2023",null=True)
    date_added = models.DateField(auto_now_add=True)
    trip_plan = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return str(self.employee)


class FlightBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)



class Expense(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null = True)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    ope_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    travel_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    flight_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    flight_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    flight_return_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    train_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    train_return_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    local_conveyance = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    place_of_visit = models.CharField(max_length = 30,null = True)
    taxi_bill = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    taxi_bill_proof = models.FileField(upload_to=get_upload_path, blank = True)

class OPEBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)

class TravelBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)

def update_budgets(sender, instance, created, **kwargs):
    if created:
        # If a new Expense object is created, update the budgets
        employee = instance.employee

        flight_budget, _ = FlightBudget.objects.get_or_create(employee=employee)
        flight_budget.remaining_budget -= instance.flight_budget_used
        flight_budget.save()

        # Update TravelBudget
        travel_budget, _ = TravelBudget.objects.get_or_create(employee=employee)
        travel_budget.remaining_budget -= instance.travel_budget_used
        travel_budget.save()

        # Update OPEBudget
        ope_budget, _ = OPEBudget.objects.get_or_create(employee=employee)
        ope_budget.remaining_budget -= instance.ope_budget_used
        ope_budget.save()


post_save.connect(update_budgets, sender=Expense)
