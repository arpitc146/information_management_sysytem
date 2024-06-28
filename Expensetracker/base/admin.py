from django.contrib import admin
from .models import *

# Register your models here.





class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("Emp_name","email","contract_no","contract_start_date","contract_start_date")
    search_fields = ['Emp_name','contract_no']

class AdvancedTravelPlanAdmin(admin.ModelAdmin):
    list_display = ("employee","month","year","date_added")
    search_fields = ['month','year']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("employee","from_date","to_date","place_of_visit")
    search_fields = ['employee__Emp_name','from_date','to_date']

class FlightBudgetAdmin(admin.ModelAdmin):
    list_display = ("employee","from_date","to_date","allocated_budget","remaining_budget")
    search_fields = ['employee__Emp_name','from_date','to_date']

class TravelBudgetAdmin(admin.ModelAdmin):
    list_display = ("employee","from_date","to_date","allocated_budget","remaining_budget")
    search_fields = ['employee__Emp_name','from_date','to_date']

class OPEBudgetAdmin(admin.ModelAdmin):
    list_display = ("employee","from_date","to_date","allocated_budget","remaining_budget")
    search_fields = ['employee__Emp_name','from_date','to_date']
    
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(FlightBudget,FlightBudgetAdmin)
admin.site.register(OPEBudget,OPEBudgetAdmin)
admin.site.register(TravelBudget,TravelBudgetAdmin)
admin.site.register(Expense,ExpenseAdmin)
admin.site.register(AdvancedTravelPlan,AdvancedTravelPlanAdmin)
