from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request, 'home.html')

# movie
def movie(request):
    return render(request, 'movie.html')

# web
def web(request):
    return render(request, 'web.html')

# Subscription
def subs(request):
    return render(request, 'subs.html')

# login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        admin_email='anam@gmail.com'
        admin_password= 'anam'

        if email == admin_email and password == admin_password:

                return redirect('admindash')
        else:
             err_msg="email and password not match"
             return render(request,'login.html',{'err_msg':err_msg})
        
    return render(request, 'login.html')

# admindashbaord
def admindash(request):
    return render(request, 'admindash.html')




