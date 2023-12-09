from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
# Create your views here.

def index(request):
    return render(request,'developer_base.html')
 

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
                if user.is_staff==True:
                    return redirect('/admin',{'user',user})  
                elif user.is_admin==True:
                    return redirect('/admin',{'user',user})
            else:
                lg_form=login_form()
                messages.info(request,'Opps...! User does not exist... Please try again..!')
    return render(request,'login.html',{'form':lg_form})


def logout(request):
    DeleteSession(request)
    return redirect('/login')


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


