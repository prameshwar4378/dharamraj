
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
  path('dashboard/',dashboard, name='developer_dashboard'),  
  path('state_list/',state_list, name='developer_state_list'), 
  path('delete_state/<int:id>',delete_state, name='developer_delete_state'), 
  path('state_bulk_creation/',state_bulk_creation, name='developer_state_bulk_creation'), 
  path('user_list/',user_list, name='developer_user_list'), 
  path('update_user/<int:id>',update_user, name='developer_update_user'), 
  path('upload_backup_file/',upload_backup_file, name='developer_upload_backup_file'), 
  path('create_backup_file/',create_backup_file, name='developer_create_backup_file'), 
  path('generate_csv_backup/',generate_csv_backup, name='developer_generate_csv_backup'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    