from django.utils import timezone
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail,  EmailMessage
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
import requests
from googleplaces import GooglePlaces, types, lang
from .models import Category, Product
from cart.forms import CartAddProductForm
from watson_developer_cloud import LanguageTranslatorV3
import json
from django.contrib.auth.decorators import login_required

def home(request):
        return render(request, 'portfolio/home.html',
                 {'portfolio': home})

def abc(request):
    return render(request, 'portfolio/abc.html',
                {'portfolio': abc})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'])
            #return HttpResponseRedirect('/')
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def register_success(request):
    return render(request, 'registration/success.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'portfolio/home.html',{'portfolio': home})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def maps(request):
    return render(request, 'portfolio/maps.html',)

def search(request):

    if 'q' in request.GET:
        locationname = request.GET['q']
        main_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=pharmacies+in+'
        api_key = '&key=AIzaSyDiyltsPQYsKOl4uXGOQjO5BAccUoV-RqU'
        url = main_api + locationname + api_key
        maps = requests.get(url).json()
        a = maps['results'][0]['formatted_address']
        a1 = maps['results'][1]['formatted_address']
        a2 = maps['results'][2]['formatted_address']
        a3 = maps['results'][3]['formatted_address']
        a4 = maps['results'][4]['formatted_address']

        b = maps['results'][0]['name']
        b1 = maps['results'][1]['name']
        b2 = maps['results'][2]['name']
        b3 = maps['results'][3]['name']
        b4 = maps['results'][4]['name']

        c = maps['results'][0]['rating']
        c1 = maps['results'][1]['rating']
        c2 = maps['results'][2]['rating']
        c3 = maps['results'][3]['rating']
        c4 = maps['results'][4]['rating']

        api_key2 = 'AIzaSyAlB4KhIzTzwR8LoN3LtjOD5_SiPO--DIE'

    return render(request, 'portfolio/maps.html', {'location': locationname, 'api':api_key2,'a':a,'a1':a1,'a2':a2,'a3':a3,'a4':a4,'b':b,'b1':b1,'b2':b2,'b3':b3,'b4':b4,'c':c,'c1':c1,'c2':c2,'c3':c3,'c4':c4,})


def parse_medicine(med_symptom, med_name, json_data):
    medDict = {}
    if med_name != "":
        drug_details = json_data['results'][0]
        openfda = [drug_details.get('openfda')]
        if openfda is not None and len(openfda) >= 1:
            if openfda[0] != {}:
                if 'generic_name' in openfda[0]:
                    medDict['Generic Name'] = (openfda[0].get('generic_name'))[0]
                if 'brand_name' in openfda[0]:
                    medDict.update({'Brand Name': (openfda[0].get('brand_name'))[0]})
                if 'purpose' in drug_details:
                    medDict.update({'Purpose': (drug_details.get('purpose'))[0]})
                if 'questions' in drug_details:
                    medDict.update({'Questions ?': (drug_details.get('questions'))[0]})
                if 'substance_name' in openfda[0]:
                    medDict.update({'Substance Name': (openfda[0].get('substance_name'))[0]})
                if 'active_ingredient' in drug_details:
                    medDict.update({'Active Ingredient': (drug_details.get('active_ingredient'))[0]})
                if 'inactive_ingredient' in drug_details:
                    medDict.update({'Inactive Ingredient': (drug_details.get('inactive_ingredient'))[0]})
                if 'dosage_and_administration' in drug_details:
                    medDict.update({'Dosage & Administration': (drug_details.get('dosage_and_administration'))[0]})
                if 'route' in openfda[0]:
                    medDict.update({'Route': (openfda[0].get('route'))[0]})
                if 'indications_and_usage' in drug_details:
                    medDict.update({'Indication & Usage': (drug_details.get('indications_and_usage'))[0]})
                if 'ask_doctor' in drug_details:
                    medDict.update({'Ask Doctor ': (drug_details.get('ask_doctor'))[0]})
                if 'ask_doctor_or_pharmacist' in drug_details:
                    medDict.update({'Ask Pharmacist ': (drug_details.get('ask_doctor_or_pharmacist'))[0]})
                if 'warnings' in drug_details:
                    medDict.update({'Warning': (drug_details.get('warnings'))[0]})
                if 'stop_use' in drug_details:
                    medDict.update({'Stop Use': (drug_details.get('stop_use'))[0]})
                dontuse = ''
                if 'do_not_use' in drug_details:
                    dontuse = (drug_details.get('do_not_use'))[0]
                    medDict.update({'Do Not Use': dontuse})
                if 'pregnancy_or_breast_feeding' in drug_details:
                    dontuse = dontuse + (drug_details.get('pregnancy_or_breast_feeding'))[0]
                    medDict.update({'Do Not Use': dontuse})
    elif med_symptom != "":
        for i in range(5):
            drug_details = json_data['results'][i]
            openfda = [drug_details.get('openfda')]
            if openfda is not None and len(openfda) >= 1:
                if openfda[0] != {}:
                    gen_name_val = ''
                    gen_name = (openfda[0].get('generic_name'))[0]
                    print('gen_name--',gen_name)
                    if ',' in gen_name:
                        gen_name_val = gen_name.split(',')[0]
                    else:
                        gen_name_val = gen_name

                    medDict.update({gen_name_val: (drug_details.get('purpose'))[0]})
    return medDict


def medicine_detail(request, med_name):
    medDict = {}
    form = MedicineForm()
    api_url_base = 'https://api.fda.gov/drug/label.json?search=openfda.generic_name:'
    search_val = med_name
    limit_cnt = '&limit=1'
    display = 'Medicine'
    med_symptom = ''
    api_url = api_url_base + search_val + limit_cnt
    print(api_url)
    json_data = requests.get(api_url).json()
    if json_data is not None:
        if 'error' in json_data:
            return render(request, 'portfolio/medicine.html',
                          {'form': form, 'medDict': medDict, 'display': 'None', "error": 'True'})
        else:
            medDict = parse_medicine(med_symptom, med_name, json_data)

    return render(request, 'portfolio/medicine.html',
                  {'form': form, 'medDict': medDict, 'display': display, "error": "False"})


def search_medicine(request):
    medDict = {}
    display = 'None'

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            med_name = cd['med_name']
            med_symptom = cd['med_symptom']
            print(med_name)
            print(med_symptom)
            api_url_base = 'https://api.fda.gov/drug/label.json?search='
            if med_name != "":
                search_para = 'openfda.generic_name:'
                search_val = med_name
                limit_cnt = '&limit=1'
                display = 'Medicine'
            elif med_symptom != "":
                search_para = 'purpose:'
                search_val = med_symptom
                limit_cnt = '&limit=5'
                display = 'Symptom'

            api_url = api_url_base + search_para + search_val + limit_cnt
            print(api_url)
            json_data = requests.get(api_url).json()
            if json_data is not None:
                if 'error' in json_data:
                    return render(request, 'portfolio/medicine.html',
                                  {'form': form, 'medDict': medDict, 'display': 'None', "error": 'True'})
                else:
                    medDict = parse_medicine(med_symptom, med_name, json_data)

            return render(request, 'portfolio/medicine.html', {'form': form, 'medDict': medDict, 'display': display, "error": "False"})
    else:
        form = MedicineForm()
    return render(request, 'portfolio/medicine.html', {'form': form, 'medDict': medDict, 'display': display, "error": "False"})


def home2(request):
    return render(request, 'portfolio/home2.html', )


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                    'shop/product/list.html',
                    {'category': category,
                    'categories': categories,
                    'products': products})


language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_apikey='ZrxokU3Cg_vKweP0hSKml_TPxpwJNe4hpKoxgAv0jcoc')

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    translation = language_translator.translate(
        text=product.description, model_id='en-es').get_result()
    obj = (json.dumps(translation, indent=2, ensure_ascii=False))
    print(obj)
    obj2 = json.loads(obj)
    product.obj2 = obj2['translations'][0]['translation']
    return render(request,
                    'shop/product/detail.html',
                    {'product': product,
                     'cart_product_form': cart_product_form})



