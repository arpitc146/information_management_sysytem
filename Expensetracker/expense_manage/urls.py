from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import *
from django.urls import include



admin.site.site_header = 'Inductus | Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',loginview,name = "login"),
    path('logout/',logoutview,name="logout"),
    path('',EmployeeView,name = "employees"),
    path('employee/<str:pk>/',EmployeeProfileView,name = "employee"),
    path('employee/<str:pk>/atp/',AdvancedTravelPlanView,name='atp'),
    path('search/',Search,name = "search"),
    path('employee/<str:pk>/tp',ActualTravelPlan,name ="tp"),
    path('employee/<str:pk1>/tp/<str:pk2>/',ViewAtp,name = "viewatp"),
    
    path('myapp/', include('myapp.urls', namespace='myapp_unique')),
    path('consultant/', include('myapp.urls')),
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)