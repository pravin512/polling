from django.urls import path

from . import views

app_name = "myapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('export_excel_file', views.export_excel_file, name='export_excel_file'),
    path('export_excel_file_template', views.export_excel_file_template, name='export_excel_file_template'),
]
