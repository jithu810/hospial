from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import ModelForm



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']


class PharmacistUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PharmacistForm(forms.ModelForm):
    class Meta:
        model=models.Pharmacist
        fields=['address','mobile','status','profile_pic']



#for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']






class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




class DateInput(forms.DateInput):
    input_type = "date"

class StockForm(forms.ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=models.Stock
        fields='__all__'
        exclude=['valid_from','reorder_level','receive_quantity', 'prescrip_drug_acess']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields='__all__'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model=models.Prescription
        fields='__all__' 

class CustomerForm(ModelForm):
    class Meta:
        model=models.Pharmacist
        fields='__all__'
        exclude=['admin','gender','mobile','address']


class DispenseForm(ModelForm):
   
   
    class Meta:
        model=models.Dispense
        fields='__all__'
        exclude=['stock_ref_no']
        
   
 
class ReceiveStockForm(ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=models.Stock
        fields='__all__'
        exclude=['category' ,'drug_name','valid_from','dispense_quantity','reorder_level','date_from','date_to','quantity','manufacture']


class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = models.Stock
		fields = ['reorder_level']
