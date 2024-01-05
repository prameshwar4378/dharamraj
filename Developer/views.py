from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import pandas as pd

# Create your views here.
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/developer/dashboard')
            elif request.user.is_admin:
                return redirect('/admin/dashboard')
            elif request.user.is_staff:
                return redirect('/staff/dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def index(request):
    return render(request,'index.html')
 
@unauthenticated_user
def login(request): 
    lg_form=login_form() 
    if request.method=='POST': 
        print("Success")
        if 'username' in request.POST: 
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                authlogin(request,user)
                if user.is_superuser==True:
                    print("is superuser")
                    return redirect('/developer/dashboard',{'user',user})  
                elif user.is_admin==True:
                    print("is admin")
                    return redirect('/admin/dashboard',{'user',user}) 
                elif user.is_staff==True:
                    print("is staff")
                    return redirect('/staff/dashboard',{'user',user})
            else:
                print("User not exist")
                lg_form=login_form()
                messages.info(request,'Opps...! User does not exist... Please try again..!')
        else:
            print("Login Missing")

    return render(request,'login.html',{'form':lg_form})


def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')
# backup_utils.py


from django.core.management import call_command
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

def delete_old_files_in_directory(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f'Files in {directory} deleted successfully.')
    except Exception as e:
        print(f'Error deleting files: {str(e)}')

@csrf_exempt
def create_backup_file(request):
    try:
        backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        os.makedirs(backup_dir, exist_ok=True)
        delete_old_files_in_directory(backup_dir)

        backup_file_path = os.path.join(backup_dir, f'backup_all_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.json')

        with open(backup_file_path, 'w') as backup_file:
            # Use call_command to run the dumpdata command for all apps
            call_command('dumpdata', '--indent', '2', stdout=backup_file)

        response_data = {'success': True, 'message': 'Backup created successfully.'}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}
    return JsonResponse(response_data)

Base_Dir = settings.BASE_DIR  # Use settings.BASE_DIR directly

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.join(Base_Dir, 'service_account.json')  # Correct file path
PARENT_FOLDER = '1ZCNxFOPEGPLZVxe-w-kTv1EGqskryOg7'

def google_drive_authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

@csrf_exempt
def upload_backup_file(request):
    try:
        # Call create_backup_file function to generate backup file
        create_backup_file(request)

        backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        json_file_names = [f for f in os.listdir(backup_dir) if f.endswith('.json') and os.path.isfile(os.path.join(backup_dir, f))]

        if not json_file_names:
            # Handle the case where no JSON file is found
            raise Exception('No backup file found.')

        file_path = os.path.join(backup_dir, json_file_names[0])  # Correct file path

        creds = google_drive_authenticate()

        service = build('drive', 'v3', credentials=creds)

        current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        file_metadata = {
            'name': current_datetime,
            'parents': [PARENT_FOLDER]
        }

        media = MediaFileUpload(file_path)

        files = service.files().create(
            body=file_metadata,
            media_body=media
        ).execute() 
        response_data = {'success': True, 'message': 'Backup uploaded successfully.'}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}
    return JsonResponse(response_data)



def user_list(request):
    user_rec=CustomUser.objects.select_related()
    if request.method == 'POST':
        form = User_Creation(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'User Created Successfully ...!')
            return redirect('/developer/user_list/')
    else:
        form = User_Creation()

    return render(request, 'developer__user_list.html', {'form': form,'user_rec':user_rec})
 
  
def update_user(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=User_Updation(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'User Updated Successfully') 
            return redirect('/developer/user_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=User_Updation(instance=pi)
    return render(request,'developer__update_user.html',{'form':fm})   


def dashboard(request):
    return render(request,'developer__dashboard.html')

def state_list(request):
    state_rec=State.objects.all()
    if request.method=="POST":
        state=request.POST.get('txt_state')
        State(state_name=state).save()
        return redirect('/developer/state_list/')
    return render(request,'developer__state_list.html',{'state_rec':state_rec})


def delete_state(request, id):
    state = get_object_or_404(State, id=id)
    state.delete()
    messages.success(request, 'State Deleted Success')
    return redirect('/developer/state_list/')


import openpyxl 
    
def state_bulk_creation(request):
    if request.method == "POST":
        excel_file = request.FILES.get('excel_file')
        if excel_file:
            try:
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active 
                data_to_insert = []
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    state_name = row[0] 
                    # Add more fields if you have more columns in the Excel file
                    if state_name:
                        print(state_name)
                        data_to_insert.append(State(state_name=state_name))
                
                State.objects.bulk_create(data_to_insert)
                messages.success(request, 'Data Imported and Updated Successfully')
            except Exception as e:
                messages.error(request, f'Error occurred during import: {str(e)}')
        else:
            messages.error(request, 'No file selected.')
        return redirect('/developer/state_list/')
    
    
from django.apps import apps
from django.utils import timezone

def convert_to_unaware_datetime(value):
    if value:
        # Convert datetime to the local timezone
        local_datetime = value.astimezone(timezone.get_current_timezone())
        # Make the datetime timezone-unaware
        return local_datetime.replace(tzinfo=None)
    return None

def generate_csv_backup(request):
    # Get the app configuration for the 'Developer' app
    app_config = apps.get_app_config('Developer')

    # Get all models in the 'Developer' app
    app_models = app_config.get_models()

    # Create a Pandas Excel writer using the xlsxwriter engine
    with pd.ExcelWriter('backup_file.xlsx', engine='xlsxwriter') as writer:
        for model in app_models:
            # Convert model data to a DataFrame
            model_data = pd.DataFrame(list(model.objects.all().values()))

            # Convert datetime fields to timezone-unaware
            for column in model_data.select_dtypes(include=['datetime64[ns]']).columns:
                model_data[column] = model_data[column].apply(convert_to_unaware_datetime)

            # Write the DataFrame to a sheet in the Excel file
            model_data.to_excel(writer, sheet_name=model.__name__, index=False)

if __name__ == "__main__":
    generate_csv_backup()