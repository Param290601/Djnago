from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import *
from django.template import loader
from django.http import HttpResponse
from .forms import OrderForm,CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .decorators import unauthenticated_user,allowed_user,admin_only
from django.contrib.auth.models import Group
import uuid
from .helpers import send_forget_password_email

@login_required(login_url='login')
@admin_only
def home(request):
    # superusers = User.objects.filter(is_superuser=True) 
    # name = Customer.objects.filter(name__startswith='P').values()
    # order = Customer.objects.all().order_by('-name').values()
    # mydata = Customer.objects.filter(name__icontains='dik').values()
    # mydata = Customer.objects.filter(name__endswith='m').values()
    # mydata = Customer.objects.filter(name__exact='Parma').values()
    # mydata = Customer.objects.filter(name__in=['Parm', 'Linus', 'hardik']).values()
    # mydata = Product.objects.filter(id__gte=3).values()
    # data1 = Customer.objects.filter(order__status = 'Delivered')
    # data2 = Customer.objects.filter(order__date_created__year='2021')
    # data = Customer.order_set.filter(order__status = 'Delivered').filter(order__date_created__year='2021')
    # data3 = Customer.objects.filter(pk=1).update(name = 'Akshay')
    # get_or_create
    # import pdb 
    # pdb.set_trace()
    # gt = greater than
    # lt = less than
    customer = Customer.objects.all()
    orders = Order.objects.all()
    total_oreder = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pendding = orders.filter(status = 'Pending').count()
    context = {
    'orders':orders,
    'customer': customer,
    'total_order': total_oreder,
    'delivered'  :delivered,
    'pendding' : pendding
    }
    return render(request,'practice/index.html',context)
    # return render(request,'practice/index.html')
    # return HttpRequest("Home")
@login_required(login_url='login')
@allowed_user(allowed_rolse=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_oreder = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pendding = orders.filter(status = 'Pending').count()
    context = {
        'orders' : orders,
        'total_oreder' : total_oreder,
        'delivered' : delivered,
        'pendding' : pendding
    }
    return render(request,'practice/user.html',context)

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def prodcut(request):
    
    superusers = User.objects.filter(is_superuser=True) 
    print(superusers)
    products = Product.objects.all()
    if request.method == 'GET':
        s = request.GET.get('search')
        if s!=None:
            products = products.filter(Q(name=s)|Q(category =s))

    return render(request,'practice/product.html',{"products":products, "s":s})

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    
    orders = myFilter.qs
    t_order = orders.count()
    context = {
        'customer' : customer,
        'orders' : orders,
        't_order' : t_order,
        'myFilter' : myFilter,
    }
    return render(request,'practice/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid:
            # print("***********")
            form.save()
            return redirect('/') 
        
    context = {'form' : form}
    return render(request,'practice/create_order.html',context)

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def updateOrder(request,pk):
    orders= Order.objects.get(id=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=orders)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {
        'form' : form
    }
    return render(request,'practice/create_order.html',context)

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def deleteOrder(request,pk):
    orders= Order.objects.get(id=pk)
    # form = OrderForm(instance=orders)
    if request.method =='POST':
        orders.delete()
        return redirect('/')
    context = {
        'item' : orders
    }
    return render(request,'practice/delete_order.html',context)
# Create your views here.
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        password = request.POST.get('password1')
        if len(password) < 8:
                messages.info(request,"lenght must be greater than 8")
                return redirect('register')
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            Customer.objects.create(
                user = user,
                name = username,
            )
            user.groups.add(group)
            messages.success(request,"account is created for: " +username)
            return redirect('login')
    context = {
        'form' : form,
    }
    return render(request,'practice/register.html',context)
@unauthenticated_user
def loginpage(request):
    # if request.user.is_authencticated:
    #     return redirect('home')
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            if user.groups == 'customer':
                return redirect('user-page')
            else:
                return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
    return render(request,'practice/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_rolse=['customer'])   
def settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method =='POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context ={
        'form' : form
    }
    return render(request,'practice/settings.html',context)

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).first():
            messages.success(request,'User is not found')
            return redirect('forgetpassword')
        
        # token = str(uuid.uuid4())
        user_object = User.objects.get(email=email)
        token = str(uuid.uuid4()) 
        customer = Customer.objects.get(name = user_object)

        customer.forget_password_token = token
        print(customer.forget_password_token)
        customer.save()
        send_forget_password_email(user_object.email,token)
        messages.success(request,'email has been sent')
        return redirect('forgetpassword')
    
    return render(request,'practice/forgetpassword.html')


def changepassword(request,token):

    profile_obj = Customer.objects.filter(forget_password_token=token).first()

    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.success(request,'No user id found')
            return redirect('/changepassword/{token}/') 
        
        if new_password != confirm_password:
            messages.success(request,"both password should be same")
            return redirect('/changepassword/{token}/')
        
        user_obj = User.objects.get(id = user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('login')

    context = {
        'profile_obj' : profile_obj.user.id
    }    

    return render(request,'practice/changepassword.html',context)