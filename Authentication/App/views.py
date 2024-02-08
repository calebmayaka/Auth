from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
  
def signup(request):
    # checks whether the user is authenticated, if yes then he is redirected to the homepage
    if request.user.is_authenticated:
        # this redirects
        return redirect('/')
    # it  then listens to a post request,esentially a data submission requast to the server
    if request.method == 'POST':
        # if yes then the data which isk00
        # (request.post) is takens as an arguement of the UserCreation Function
        form = UserCreationForm(request.POST)
        # it then check for a condition if the form is valid,using is_valid() method - this is the method that does validation  
        if form.is_valid():
            # if it is valid it saves the data to the database.
            form.save()
            # this function is used to retrieve the validated data, it takes an arguement of any of the validated fields
            # in this case it takes in the username and any one of the passwords, since they were same
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # the authenticate function checks the database and confirms that the credentials of the newly created user are correct.
            user = authenticate(username=username, password=password)
            # it then logs in the user, the login function takes two arguements, request and user, it creates a new session on login
            login(request, user)
            #it then redirects the user to the home page
            return redirect('/')
        else:
            # render takes at least two arguements, a requuest, the target template and form
            return render(request, 'signup.html', {'form': form})
        # if the request was not a post request then an instance of a blank usercreationform is created, which returns a render of a signup page
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

# function handling the home page
def home(request): 
    return render(request, 'home.html')
   
# function handling signin
def signin(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Wrong Username or Password'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
  # profile function
def profile(request): 
    return render(request, 'profile.html')
# signout function
def signout(request):
    logout(request)
    return redirect('/')