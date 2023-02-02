from django.shortcuts import render
from django.http import HttpRequest
from .models import *
from django.template import loader
from django.http import HttpResponse

def home(request):
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

def prodcut(request):
    products = Product.objects.all()

    return render(request,'practice/product.html',{"products":products})

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    t_order = orders.count()
    context = {
        'customer' : customer,
        'orders' : orders,
        't_order' : t_order,
    }
    return render(request,'practice/customer.html',context)

# Create your views here.
