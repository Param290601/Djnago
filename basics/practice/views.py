
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpRequest
from .models import *
from django.template import loader
from django.http import HttpResponse
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter, PoductFilter
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group
import uuid
from .helpers import send_forget_password_email
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator


class logoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(allowed_user(allowed_rolse=['customer']), name='dispatch')
@method_decorator(login_required(login_url='login'), name='dispatch')
class settings(View):
    def get(self, request):
        customer = request.user.customer
        form = CustomerForm(instance=customer)
        context = {
            'form': form
        }
        return render(request, 'practice/settings.html', context)

    def post(self, request):
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        context = {
            'form': form
        }
        return render(request, 'practice/settings.html', context)


class forgetpassword(View):
    def get(self, request):
        return render(request, 'practice/forgetpassword.html')

    def post(self, request):
        email = request.POST.get('email')

        if not User.objects.filter(email=email).first():
            messages.success(request, 'User is not found')
            return redirect('forgetpassword')

        # token = str(uuid.uuid4())
        user_object = User.objects.get(email=email)
        token = str(uuid.uuid4())
        customer = Customer.objects.get(name=user_object)

        customer.forget_password_token = token
        # print(customer.forget_password_token)
        customer.save()
        send_forget_password_email(user_object.email, token)
        messages.success(request, 'email has been sent')
        return redirect('forgetpassword')


class changepassword(View):
    def get(self, request, token):
        profile_obj = Customer.objects.filter(
            forget_password_token=token).first()
        context = {
            'profile_obj': profile_obj.user.id
        }
        return render(request, 'practice/changepassword.html', context)

    def post(self, request, token):
        profile_obj = Customer.objects.filter(
            forget_password_token=token).first()
        context = {
            'profile_obj': profile_obj.user.id
        }
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.success(request, 'No user id found')
            return render(request, 'practice/changepassword.html', context)

        l, u, p, d = 0, 0, 0, 0
        if (len(new_password) >= 8):
            for i in new_password:

                # counting lowercase alphabets
                if (i.islower()):
                    l += 1

                # counting uppercase alphabets
                if (i.isupper()):
                    u += 1

                # counting digits
                if (i.isdigit()):
                    d += 1

                # counting the mentioned special characters
                if (i == '@' or i == '$' or i == '_'):
                    p += 1
            if (l < 1 or u < 1 or p < 1 or d < 1 or l+p+u+d != len(new_password)):
                messages.success(request, "password is not valid")
                return render(request, 'practice/changepassword.html', context)
        else:
            messages.success(request, "password is short")
            return render(request, 'practice/changepassword.html', context)

        if new_password != confirm_password:
            messages.success(request, "both password should be same")
            return render(request, 'practice/changepassword.html', context)

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('login')


decorators = [admin_only, login_required(login_url='login')]
decorators1 = [login_required(login_url='login'),
               allowed_user(allowed_rolse=['admin'])]


@method_decorator(decorators, name='dispatch')
class home(ListView):
    # model = [Customer,Order]
    # model = Customer
    # template_name = 'practice/index.html'
    # model = Order
    template_name = 'practice/index.html'
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):

    #     orders = Order.objects.all()
    #     total =  orders.count()
    #     queryset = {
    #         'orders' : orders,
    #         'total_order' : total
    #     }
    #     return queryset

    # def get_context_data(self, **kwargs):

    #     return super().get_context_data(**kwargs)

    def get(self, request):
        customer = Customer.objects.all()
        orders = Order.objects.all()
        total_oreder = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pendding = orders.filter(status='Pending').count()
        if request.method == 'GET':
            s = request.GET.get('search')
            if s!=None:
                orders = orders.filter(Q(product__name__icontains=s)|Q(status__icontains=s))
            else:
                orders = Order.objects.all()
        context = {
            'orders': orders,
            'customer': customer,
            'total_order': total_oreder,
            'delivered': delivered,
            'pendding': pendding
        }
        return render(request, self.template_name, context)


@method_decorator(allowed_user(allowed_rolse=['customer']), name='dispatch')
@method_decorator(login_required(login_url='login'), name='dispatch')
class userpage(View):
    template_name = 'practice/product.html'

    def get(self, request):
        orders = request.user.customer.order_set.all()
        total_oreder = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pendding = orders.filter(status='Pending').count()
        context = {
            'orders': orders,
            'total_oreder': total_oreder,
            'delivered': delivered,
            'pendding': pendding
        }
        return render(request, self.template_name, context)


# @method_decorator(decorators1, name='dispatch')
# class product(ListView):
#     templet_name = 'practice/product.html'

#     def get(self, request):
#         context = {}
#         products = Product.objects.all()
#         product_Filter = PoductFilter(self.request.GET, queryset=products)
#         context['product_Filter'] = product_Filter
#         paginator_product = Paginator(product_Filter.qs,2,orphans=1) 
#         page_number = request.GET.get('page')
#         page_obj = paginator_product.get_page(page_number)
#         context['page_obj'] = page_obj
        
#         return render(request, self.templet_name,context = context)

@login_required(login_url='login')
@allowed_user(allowed_rolse=['admin'])
def prodcut(request):
    context = {}
    products = Product.objects.all()
    if request.method == 'GET':
            s = request.GET.get('search')
            if s!=None:
                products = products.filter(Q(name__icontains=s) | Q(company__icontains=s))
            else:
                products = Product.objects.all()
    product_Filter = PoductFilter(request.GET, queryset=products)
    ps = product_Filter.qs
    product = products.intersection(ps)
    context['product_Filter'] = product_Filter
    context['s'] = s
    paginator_product = Paginator(product,2) 
    page_number = request.GET.get('page')
    page_obj = paginator_product.get_page(page_number)
    context['page_obj'] = page_obj
    
    return render(request,'practice/product.html',context = context)

@method_decorator(decorators1, name='dispatch')
class customer(TemplateView):
    template_name = 'practice/customer.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=pk)
        orders = customer.order_set.all()

        myFilter = OrderFilter(self.request.GET, queryset=orders)

        orders = myFilter.qs
        t_order = orders.count()
        context = {
            'customer': customer,
            'orders': orders,
            't_order': t_order,
            'myFilter': myFilter,
        }
        return context


@method_decorator(decorators1, name='dispatch')
class createOrder(CreateView):

    model = Order
    form_class = OrderForm
    template_name = 'practice/create_order.html'
    success_url = '/'

    def form_valid(self, form: OrderForm):

        return super().form_valid(form)
    # def get(self,request):
    #     form = OrderForm()
    #     context = {'form' : form}
    #     return render(request,self.template_name,context)
    # def post(self,request):
    #     form = OrderForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    #         return redirect('/')

# @method_decorator(decorators1,name='dispatch')
# class updateOrder(View):
#     template_name = 'practice/create_order.html'
#     def get(self,request,pk):
#         orders= Order.objects.get(id=pk)
#         form = OrderForm(instance=orders)
#         context = {
#         'form' : form
#         }
#         return render(request,self.template_name,context)
#     def post(self,request,pk):
#         orders= Order.objects.get(id=pk)
#         form = OrderForm(request.POST,instance=orders)
#         if form.is_valid:
#             form.save()
#             return redirect('/')


@method_decorator(decorators1, name='dispatch')
class updateOrder(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'practice/create_order.html'
    success_url = '/'

    def form_valid(self, form: OrderForm):

        return super().form_valid(form)


@method_decorator(decorators1, name='dispatch')
class deleteOrder(DeleteView):
    model = Order
    template_name = 'practice/delete_order.html'
    success_url = '/'

    # def get(self,request,pk):
    #     orders= Order.objects.get(id=pk)
    #     context = {
    #     'item' : orders
    #     }
    #     return render(request,'practice/delete_order.html',context)
    # def post(self,request,pk):
    #     orders= Order.objects.get(id=pk)
    #     Order.objects.get(id=pk).delete()
    #     return redirect('/')


@method_decorator(unauthenticated_user, name='dispatch')
class register(View):
    def get(self, request):
        form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, 'practice/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        password = request.POST.get('password1')
        if len(password) < 8:
            messages.info(request, "lenght must be greater than 8")
            return redirect('register')
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            Customer.objects.create(
                user=user,
                name=username,
            )
            user.groups.add(group)
            messages.success(request, "account is created for: " + username)
            return redirect('login')


@method_decorator(unauthenticated_user, name='dispatch')
class loginpage(View):
    def get(self, request):

        return render(request, 'practice/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups == 'customer':
                return redirect('user-page')
            else:
                return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')

# @unauthenticated_user
# def loginpage(request):
#     # if request.user.is_authencticated:
#     #     return redirect('home')
#     # else:
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username,password=password)
#         if user is not None:
#             login(request,user)
#             if user.groups == 'customer':
#                 return redirect('user-page')
#             else:
#                 return redirect('home')
#         else:
#             messages.info(request,'username or password is incorrect')
#     return render(request,'practice/login.html')

# generic views contains ListViews and DetailViews

# ListView:
# list view print the list of the data using model
# DetailView:
# detail view print the particulart cutomer data which is needed
# in details view we compulsary have to pass id in url with pk or slug
# list view will print the data od that particular customer in the page
