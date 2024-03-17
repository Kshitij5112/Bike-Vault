from django.shortcuts import render , redirect
from bikeapp.models import Bike , Cart , Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail
# Create your views here.
def homeFunction(request):
    context={}
    data=Bike.objects.all()
    context['bikes']=data
    return render(request,'index.html',context)
 

def userlogin(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def userlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        context = {}
        n = request.POST['username']
        p = request.POST['password']
        if n=='' or p=='':
            context['error'] = 'Please enter all the fields'
            return render(request,'login.html',context)
        else:
            user = authenticate(username = n, password= p)
            if user is not None:
                login(request,user)
                # context['success'] = 'Logged in successfully'
                messages.success(request,'Logged in successfully !!')
                return redirect('/')
            else:
                context['error'] = 'Please provide correct details'
                return render(request,'login.html',context)
            
def userlogout(request):
    context={}
    context['success']='Logged out successfully !! '
    logout(request)
    return redirect('/')
            
def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        context = {}
        n = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpass']
        if n=='' or e=='' or p=='' or cp=='':
            context['error'] = 'Please enter all the fields'
            return render(request,'register.html',context)
        elif p != cp:
            context['error'] = 'Password and confirm password must be same !!'
            return render(request,'register.html',context)
        else:
            context['success'] = 'Registred Successfully!! Please Login'
            user = User.objects.create(username = n, email=e)
            user.set_password(p)# to set encrypted password
            user.save()
            return render(request,'login.html',context)
            
def bikedetails(request,pid):
    context = {}
    data = Bike.objects.filter(id = pid)
    context['bike'] = data[0]
    return render(request,'details.html',context)

def addtocart(request,bikeid):
    userid = request.user.id
    context= {}
    if userid is None:        
        context['error'] = 'Plaese login so as to add the item in your cart'
        return render(request,'login.html',context)
    else:
        # cart will added if item and user object is known
        userid = request.user.id
        users = User.objects.filter(id = userid)
        bikes = Bike.objects.filter(id = bikeid)
        cart = Cart.objects.create(pid = bikes[0] , uid = users[0] )
        cart.save()
        # context['success'] = 'Pet added to cart !!'
        messages.success(request,'Bike added to cart !!')
        return redirect('/')
    
def removeCart(request,cartid):
    data = Cart.objects.filter(id = cartid)
    data.delete()
    messages.success(request,'item removed from your cart')
    return redirect('/mycart')

def showMyCart(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid = userid )
    context['mycart'] = data
    count = len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'mycart.html',context)

def confirmorder(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid = userid )
    context['mycart'] = data
    count = len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'conforder.html',context)

def makepayment(request):
    context={}
    userid=request.user.id
    data=Cart.objects.filter(uid=userid)
    total=0
    for cart in data:
        total+=cart.pid.price*cart.quantity
    client=razorpay.Client(auth=("rzp_test_VMkJbg8RZgdNCO","gynOYLfqQhN9KtgCWxrEhWCZ"))
    data={"amount": total*100,"currency":"INR","receipt":""}
    payment=client.order.create(data=data)
    print(payment)
    context['data']=payment
    return render (request,'pay.html',context)

def sortBikesByPrice(request,dir):
    col=''
    context = {}
    if dir == 'asc':
        col='price'
    else:
        col='-price'
    data = Bike.objects.all().order_by(col)
    context['bikes'] = data
    return render(request,'index.html',context)

def searchBikeByType(request,val):
    context={}    
    data = Bike.objects.filter(type = val )
    context['bikes'] = data
    return render(request,'index.html',context)

def searchBike(request,val):
    context={}    
    data = Bike.objects.filter(type = val )
    context['bikes'] = data
    return render(request,'index.html',context)


def rangeofprice(request):
    context = {}
    min = request.GET['min']
    max =request.GET['max']
    c1 = Q(price__gte = min)
    c2 = Q(price__lte = max)
    data = Bike.objects.filter(c1 & c2)
    context['bikes'] = data
    return render(request,'index.html',context)

def placeorder(request):
    userid=request.user.id
    user=User.objects.filter(id=userid)
    mycart=Cart.objects.filter(uid=userid)
    ordid=random.randrange(10000,99999)
    for cart in mycart:
        pet=Bike.objects.filter(id=cart.pid.id)
        ord=Order.objects.create(uid=user[0],pid=pet[0],quantity=cart.quantity,orderid=ordid)
        ord.save()
    mycart.delete()
    
    msg_body = 'Order id is:'+str(ordid)
    custEmail = request.user.email1
    send_mail(
    "Order placed successfully!!", #subject
    msg_body, 
    "kshitij.warankar@gmail.com", #from
    [custEmail],
    fail_silently=False,
    )    

    
    messages.success(request,'order placed successfully')
    return redirect('/')