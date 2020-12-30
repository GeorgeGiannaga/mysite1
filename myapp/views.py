
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="app")
import timezonefinder, pytz
import datetime
from myapp.models import User_insertion
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

@login_required(login_url="/login")
def home(request):
    return render(request, template_name='base.html')

@login_required(login_url = "/login")
def new_search(request):
    search = request.POST.get('search')
    c = geoloc({search})
    if c:
        tf = timezonefinder.TimezoneFinder()
        tz_str = tf.certain_timezone_at(lat=c[0], lng=c[1])
        timezone = pytz.timezone(tz_str)
        dt = datetime.datetime.utcnow()
        stuff = {
            'search': ("The date/time in %s is %s" % (c[2], dt + timezone.utcoffset(dt))),
            }
        return render(request, template_name='myapp/new_search.html', context=stuff)
    else:
        messages.success(request, "Please enter a city or a place that exists in this world")
        return render(request, template_name='base.html')

def geoloc(city= None):
    if city != None:
        try:
            loc = geolocator.geocode(str(city))
            b = str(loc.address).split(", ")
            return (loc.latitude, loc.longitude, b[0])
        except:
            return None

@unauthorized_user
def register(request):
    if request.method == "POST":
        try:
            Username = request.POST["Username"]
            email = request.POST["email"]
            Password1 = request.POST["Password1"]
            Password2 = request.POST["Password2"]
            if Password1 != Password2 and request.method == "POST":
                messages.success(request, "The two passwords do not match, try again")
                return render(request, "register/register.html")
            User.objects.create_user(username = Username,email = email, password = Password1)
            return render(request, "base.html")
        except:
            messages.success(request, "Username or email is already being used by another user. Please try again with a different email/username")
            return render(request, "register/register.html")
    else:
        return render(request, "register/register.html")

@unauthorized_user
def log_in(request):
    if request.method == "POST":
        user = authenticate(username = request.POST.get('Username'), password = request.POST.get('password'))
        if user is not None:
            login(request, user)
            return render(request, "base.html")
        else:
            messages.success(request, "Username or Password not valid!! Please try again")
            return render(request, "login/login.html")
    if request.method == "GET":
        return render(request, "login/login.html")

@login_required(login_url = "/login")
def proper(request):
    if request.method == 'POST':
        last_name = request.POST.get("Last_name")
        first_name = request.POST.get("First_name")
        country = request.POST.get("Country")
        city = request.POST.get("City")
        address = request.POST.get("Address")
        description = request.POST.get("Description")
        new_property = User_insertion(Last_name=last_name, First_name=first_name, Country=country, City=city, Address=address, Description=description, user=request.user)
        new_property.save()
        messages.success(request, "Your property has been saved successfully, your house will be displayed for sale in our site!")
        return render(request, "property/property.html")
    else:
        return render(request, "property/property.html")


def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully. If you want to continue you have to login again!!")
    return redirect('log_in')

@login_required(login_url = "/login")
def render_pdf_view(request):
    if request.method == 'GET':
        properties = User_insertion.objects.filter(user=request.user).all()
        context = {'properties': properties}
        template = get_template('pdfile.html')
        context_p = template.render(context)
        response = BytesIO()
        pisa_status = pisa.pisaDocument(BytesIO(context_p.encode('UTF-8')), response)
        if not pisa_status.err:
            return HttpResponse(response.getvalue(), content_type="application/pdf")
        else:
            return HttpResponse("We had some errors , please try again later")
    else:
        HttpResponse("Unknown method , not recognised")

@login_required(login_url= '/login')
def ProperVeiw(request):
    properties = User_insertion.objects.filter(user=request.user).all()
    context = {'properties': properties}
    return render(request, 'properview.html', context)

@login_required(login_url= '/login')
def editproper(request, id):
    properties = User_insertion.objects.filter(user=request.user).get(id=id)
    if request.method == 'POST':
        last_name = request.POST.get("Last_name")
        first_name = request.POST.get("First_name")
        country = request.POST.get("Country")
        city = request.POST.get("City")
        address = request.POST.get("Address")
        description = request.POST.get("Description")
        User_insertion.objects.filter(id = id, user=request.user).update(Last_name=last_name, First_name=first_name, Country=country, City=city, Address=address, Description=description)
        messages.success(request, "Your property's attributes have been updated!!")
        properties = User_insertion.objects.filter(user=request.user).get(id=id)
        return render(request, 'editproper.html', {'properties': properties})
    else:
        return render(request, 'editproper.html', {'properties': properties})

@login_required(login_url='/login')
def deleteproper(request, id):
    properties = User_insertion.objects.filter(user=request.user).get(id=id)
    if request.method == 'POST':
        properties.user.delete()
        messages.success(request, "Your property's has been deleted successfully")
        return redirect('properviews')
    else:
        return redirect('properviews')
