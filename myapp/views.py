
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="app")
import timezonefinder, pytz
import datetime
from django.conf import settings
from myapp.models import Property, Details
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO




def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search')
    properties = Property.objects.filter(City=search).all() or Property.objects.filter(Country=search).all()
    details = Details.objects.all()
    content = {
        'details':details,
        'search': search,
        'properties': properties,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'myapp/new_search.html', context=content)


def geoloc(address= None):
    if address != None:
        try:
            loc = geolocator.geocode(str(address))
            return (loc.latitude, loc.longitude)
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
            return redirect("log_in")
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
        post_code = request.POST.get("Post_Code")
        description = request.POST.get("Description")
        price = request.POST.get("Price")
        image = request.FILES.get("Image")
        new_property = Property(Last_name=last_name, First_name=first_name, Country=country, City=city, Address=address, Post_Code=post_code, Price=price, Description=description, Image = image, user=request.user)
        if Property.objects.filter(user= request.user, Address = address).exists():
            messages.success(request, "We already have the attributes of this property, try update them instead")
        else:
            messages.success(request, "Your property has been saved successfully, your house will be displayed for sale in our site!")
            new_property.save()
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
        properties = Property.objects.filter(user=request.user).all()
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
    properties = Property.objects.filter(user=request.user).all()
    context = {'properties': properties}
    return render(request, 'properview.html', context)

@login_required(login_url= '/login')
def editproper(request, id):
    properties = Property.objects.filter(user=request.user).get(id=id)
    if request.method == 'POST':
        last_name = request.POST.get("Last_name")
        first_name = request.POST.get("First_name")
        country = request.POST.get("Country")
        city = request.POST.get("City")
        address = request.POST.get("Address")
        post_code = request.POST.get("Post_Code")
        price = request.POST.get("Price")
        description = request.POST.get("Description")
        Property.objects.filter(id = id, user=request.user).update(Last_name=last_name, First_name=first_name, Country=country, City=city, Address=address, Post_code = post_code, Price = price, Description=description)
        messages.success(request, "Your property's attributes have been updated!!")
        properties = Property.objects.filter(user=request.user).get(id=id)
        return render(request, 'editproper.html', {'properties': properties})
    else:
        return render(request, 'editproper.html', {'properties': properties})

@login_required(login_url='/login')
def deleteproper(request, id):
    property = Property.objects.filter(user=request.user).get(id=id)
    if request.method == 'POST':
        property.Image.delete(save=False)
        property.delete()
        messages.success(request, "Your property has been deleted successfully")
        return redirect('properviews')
    else:
        return redirect('properviews')


def description(request, pk):
    desc = Property.objects.get(pk=pk)
    address = Property.objects.values('Address').get(pk=pk)['Address']
    detail = desc.details
    add1 = float(geoloc(address=address)[0])
    add2 = float(geoloc(address=address)[1])
    content= {
        'detail':detail,
        'add1': add1,
        'add2': add2,
        'desc': desc,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'Description.html', context=content)

@login_required(login_url='/login')
def detailsave(request):
    properties = Property.objects.filter(user=request.user).all()
    if request.method == 'POST':
        property_id =request.POST.get('property_id')
        floors = request.POST.get('Floors')
        garden = request.POST.get("Garden") or False
        furnised = request.POST.get("Furnised") or False
        view = request.POST.get("View")
        altitude = request.POST.get("Altitude")
        near_places = request.POST.get("Near_places")
        balconies = request.POST.get("Balconies")
        windows = request.POST.get("Windows")
        light = request.POST.get("Light") or False
        det = Details(property_id=property_id, Floors = floors, Garden = garden, Furnised = furnised, View = view, Altitude = altitude, Near_places = near_places, Balconies = balconies, Windows = windows, Light = light)
        messages.success(request, "Your property's details have been added to your property's attributes!!")
        det.save()
    return render(request, 'Details.html', {'properties': properties})


@login_required(login_url='/login')
def ViewDetails(request):
    properties = Property.objects.filter(user=request.user).all()
    context = {}
    for property in properties:
        detail = property.details
        context[property.id] = {'detail' : detail, 'address' : property.Address}
    return render(request, 'Viewdetails.html', {'context': context})


@login_required(login_url='/login')
def Edetails(request, id):
    details = Details.objects.get(property_id=id)
    if request.method == 'POST':
        floors = request.POST.get('Floors')
        garden = request.POST.get("Garden") or False
        furnised = request.POST.get("Furnised") or False
        view = request.POST.get("View")
        altitude = request.POST.get("Altitude")
        near_places = request.POST.get("Near_places")
        balconies = request.POST.get("Balconies")
        windows = request.POST.get("Windows")
        light = request.POST.get("Light") or False
        Details.objects.filter(property_id=id).update(Floors = floors, Garden = garden, Furnised = furnised, View = view, Altitude = altitude, Near_places = near_places, Balconies = balconies, Windows = windows, Light = light)
        details = Details.objects.get(property_id=id)
        messages.success(request, "Your property's details have been updated!!")
        content = {
            'details': details,
        }
        return render(request, 'EditDetails.html', content)
    else:
        content = {
            'details': details,
        }
        return render(request, 'EditDetails.html', content)

