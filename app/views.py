from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
   user_id = request.session.get('user_id')
   if user_id:
       try:
           user = User.objects.get(id=user_id)
           return render(request, 'index.html', {'user': user})
       except User.DoesNotExist:
           pass
   return render(request, 'index.html')

def home(request):
    user_id = request.session.get('user_id')
    if user_id:
       try:
           user = User.objects.get(id=user_id)
           return render(request, 'home.html', {'user': user})
       except User.DoesNotExist:
           pass
    return render(request, 'home.html')

def movie(request):
    user_id = request.session.get('user_id')
    if user_id:
       try:
           user = User.objects.get(id=user_id)
           return render(request, 'movie.html', {'user': user})
       except User.DoesNotExist:
           pass
    return render(request, 'movie.html')

def web(request):
    user_id = request.session.get('user_id')
    if user_id:
       try:
           user = User.objects.get(id=user_id)
           return render(request, 'web.html', {'user': user})
       except User.DoesNotExist:
           pass
    return render(request, 'web.html')

# Subscription
def subs(request):
    user_id = request.session.get('user_id')
    subscription = Subscription.objects.all

    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return render(request,'subs.html',{'user':user,'subscription':subscription})
        except User.DoesNotExist:
            pass
    return render(request,'subs.html',{'subscription':subscription})

# profile
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
        return render(request,'profile.html',{'user':user})
    except User.DoesNotExist:
        return redirect('login')

# login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Admin login
        admin_email = 'anam@gmail.com'
        admin_password = 'anam'
        
        if email == admin_email and password == admin_password:
            request.session['user_id'] = 'admin'
            request.session['user_type'] = 'admin'
            return redirect('admindash')
        
        # User login
        try:
            user = User.objects.get(email=email)
            
            # Check password
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['user_type'] = 'user'
                return redirect('home')
            else:
                err_msg = "Wrong password"
        except User.DoesNotExist:
            err_msg = "Email not found"
        
        return render(request, 'login.html', {'err_msg': err_msg})
        
    return render(request, 'login.html')
        

# admindashbaord
def admindash(request):
    # Get all users and subscriptions
    all_users = User.objects.all()
    all_subscriptions = Subscription.objects.all()
    
    # Handle POST requests
    if request.method == 'POST':
        # Determine which form was submitted
        submitted_form = request.POST.get('form')
        
        # Handle user creation
        if submitted_form == 'user':
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            new_password = request.POST.get('password')
            password_check = request.POST.get('confirm_password')
            
            # Validate the passwords match
            if new_password != password_check:
                context = {
                    'message': 'Password confirmation failed', 
                    'status': 'error',
                    'users': all_users,
                    'subscriptions': all_subscriptions
                }
                return render(request, 'admindash.html', context)
            
            # Check for existing users with same email
            existing_user = User.objects.filter(email=new_email)
            if existing_user:
                context = {
                    'message': 'This email is already in use', 
                    'status': 'error',
                    'users': all_users,
                    'subscriptions': all_subscriptions
                }
                return render(request, 'admindash.html', context)
                
            # All validations passed, create the user
            new_user = User()
            new_user.username = new_username
            new_user.email = new_email
            new_user.password = new_password
            new_user.user_type = 'user'
            new_user.save()
            
            # Get updated user list
            all_users = User.objects.all()
            
            context = {
                'message': 'New user was created successfully', 
                'status': 'success',
                'users': all_users,
                'subscriptions': all_subscriptions
            }
            return render(request, 'admindash.html', context)
            
        # Handle subscription creation    
        elif submitted_form == 'subscription':
            sub_plan = request.POST.get('plan_name')
            sub_price = request.POST.get('price')
            sub_features = request.POST.get('features')
            sub_duration = request.POST.get('duration')
            
            # Create new subscription plan
            new_sub = Subscription()
            new_sub.plan_name = sub_plan
            new_sub.price = sub_price
            new_sub.features = sub_features
            new_sub.duration = sub_duration
            new_sub.save()
            
            # Get updated subscription list
            all_subscriptions = Subscription.objects.all()
            
            context = {
                'message': 'New subscription plan was added', 
                'status': 'success',
                'users': all_users,
                'subscriptions': all_subscriptions
            }
            return render(request, 'admindash.html', context)
    
    # Handle GET requests
    context = {
        'users': all_users,
        'subscriptions': all_subscriptions
    }
    return render(request, 'admindash.html', context)


def logout(request):
    # Clear the session
    request.session.clear()
    # Force session save
    request.session.modified = True
    # Redirect to login page
    return redirect('login')

# In views.py

def edit_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            # Update user data
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            
            # Only update password if provided
            new_password = request.POST.get('password')
            if new_password:
                user.password = new_password
                
            user.save()
            return redirect('admindash')
        
        return render(request, 'edit_user.html', {'user': user})
    except User.DoesNotExist:
        return redirect('admindash')

def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
    except User.DoesNotExist:
        pass
    return redirect('admindash')

def edit_subscription(request, sub_id):
    try:
        subscription = Subscription.objects.get(id=sub_id)
        
        if request.method == 'POST':
            # Update subscription data
            subscription.plan_name = request.POST.get('plan_name')
            subscription.price = request.POST.get('price')
            subscription.features = request.POST.get('features')
            subscription.duration = request.POST.get('duration')
            subscription.save()
            return redirect('admindash')
        
        return render(request, 'edit_subscription.html', {'subscription': subscription})
    except Subscription.DoesNotExist:
        return redirect('admindash')

def delete_subscription(request, sub_id):
    try:
        subscription = Subscription.objects.get(id=sub_id)
        subscription.delete()
    except Subscription.DoesNotExist:
        pass
    return redirect('admindash')

