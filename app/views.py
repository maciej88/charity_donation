from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView


from .serializers import InstitutionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import *
from .forms import *

UserModel = get_user_model()

class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {"form": form})
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            user_check  = User.objects.filter(email=email)
            if user is not None:
                login(request, user)
            elif not user_check:
                return redirect(reverse('register'))
            else:
                msg = 'Login lub hasło są niepoprawne'
                return render(request, 'login.html', {"form": form, "msg": msg})
            # error information
            return redirect('/')
        else:
            msg = 'Login lub hasło są niepoprawne'
            return render(request, 'login.html', {"form": form, "msg": msg})

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class UserAdd(View):
    def get(self, request):
        form = UserAddForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = UserAddForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            User.objects.create_user(password=password1, email=email,
                                     first_name=first_name, last_name=last_name)
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})



class UserDetails(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user_info = User.objects.get(id=user_id)
        donations = Donation.objects.filter(user_id=request.user.id)
        ctx = {
            'user_info': user_info,
            'donations': donations,
        }
        return render(request, 'user.html', ctx)

class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'user_update.html'

    def get_object(self, **kwargs):
        return self.request.user



#Landing page View:
class MainPage(View):
    def get(self, request):
        donations = Donation.objects.all()
        quantity_of_donations = 0 #number of donated bags
        quantity_of_organizations = [] #list of organizations - len il summary whole list
        fundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        locals = Institution.objects.filter(type=3)
        for donation in donations:
            quantity_of_donations += donation.quantity
            if donation.institution not in quantity_of_organizations:
                quantity_of_organizations.append(donation.institution)
        ctx = {'fundations': fundations, 'organizatins': organizations,
               'locals': locals, 'quantity_of_donations': quantity_of_donations,
               'quantity_of_organizations': len(quantity_of_organizations)}
        return render(request, 'index.html', ctx)

    def institution_pagination(request):
        pass



#donation adding
class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories':categories, "institutions": institutions})

    def post(self, request):
        user = request.user
        categories = request.POST.getlist("categories")
        quantity = request.POST.get("bags")
        organization = request.POST.get("organization")
        adress = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        pick_up_date = request.POST.get("date")
        pick_up_time = request.POST.get("time")
        pick_up_comment = request.POST.get("more_info")
        institution = Institution.objects.get(id=organization)
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            adress=adress,
            phone_number=phone,
            city=city,
            zip_code=postcode,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user)
        donation.categories.set(categories)
        return render(request, 'form-confirmation.html')

def get_institution_by_category(request):
    category_id = request.GET.getlist('category_id')
    if category_id is not None:
        categories = Category.objects.filter(pk__in=category_id)
        institutions = Institution.objects.filter(categories__in=categories).distinct()
        print(categories)
        print(institutions)
    else:
        institutions = Institution.objects.all()
    return render(request, "api_institutions.html", {'institutions': institutions})

class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')

#REST Framework:
class InstitutionList(APIView):

    def get(self, request, format=None):
        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionView(APIView):

    def get_object(self, pk):
        try:
            return Institution.objects.get(pk=pk)
        except Institution.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        institution = self.get_object(id)
        serializer = InstitutionSerializer(institution, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        institution = self.get_object(id)
        institution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        institution = self.get_object(id)
        serializer = InstitutionSerializer(institution, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, format=None):
        pass
