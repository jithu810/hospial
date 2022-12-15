from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from blood import models as blood_models
from donor import models as donor_models
from donor import forms as donor_forms
from django.contrib.auth.models import User
from blood import forms as blood_forms
from django.contrib import messages
from django.utils import timezone
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_donor(user):
    return user.groups.filter(name='DONOR').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')

    elif is_donor(request.user):      
        return redirect('donor/donor-dashboard')







@login_required(login_url='adminlogin')
def admin_dashboard_view2(request):
    x=blood_models.Stock.objects.all()
    if len(x)==0:
        blood1=blood_models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=blood_models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=blood_models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=blood_models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=blood_models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=blood_models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=blood_models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=blood_models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()
    totalunit=blood_models.Stock.objects.aggregate(Sum('unit'))
    dict={

        'A1':blood_models.Stock.objects.get(bloodgroup="A+"),
        'A2':blood_models.Stock.objects.get(bloodgroup="A-"),
        'B1':blood_models.Stock.objects.get(bloodgroup="B+"),
        'B2':blood_models.Stock.objects.get(bloodgroup="B-"),
        'AB1':blood_models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':blood_models.Stock.objects.get(bloodgroup="AB-"),
        'O1':blood_models.Stock.objects.get(bloodgroup="O+"),
        'O2':blood_models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':donor_models.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':blood_models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':blood_models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'hospital/admin_dashboard2.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=donor_models.Donor.objects.all()
    return render(request,'hospital/admin_donor.html',{'donors':donors})


@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=donor_models.Donor.objects.get(id=pk)
    user=donor_models.User.objects.get(id=donor.user_id)
    userForm=donor_forms.DonorUserForm(instance=user)
    donorForm=donor_forms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=donor_forms.DonorUserForm(request.POST,instance=user)
        donorForm=donor_forms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'hospital/admin_update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=donor_models.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=donor_models.BloodDonate.objects.filter(status="Pending")
    return render(request,'hod_templates/donation.html',{'donations':donations})


login_required(login_url='adminlogin')
def admin_donation_history(request):
    donations=donor_models.BloodDonate.objects.all()
    return render(request,'hod_templates/view_donations.html',{'donations':donations})


@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=donor_models.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=blood_models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    messages.success(request, "Donnation Added")

    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=donor_models.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    messages.success(request, "Donnation Rejected")

    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=blood_models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'hod_templates/requests.html',{'requests':requests})



@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=blood_models.BloodRequest.objects.all()
    return render(request,'hod_templates/request_history.html',{'requests':requests})


@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=blood_models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=blood_models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        messages.success(request, "Blood Request Accepted")
        
    else:
        messages.success(request, "Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available")
    req.save()

    requests=blood_models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'hod_templates/requests.html',{'requests':requests})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=blood_models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    messages.success(request, "Blood Request Denied")
    return HttpResponseRedirect('/admin-request-history')


@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':blood_forms.BloodForm(),
        'A1':blood_models.Stock.objects.get(bloodgroup="A+"),
        'A2':blood_models.Stock.objects.get(bloodgroup="A-"),
        'B1':blood_models.Stock.objects.get(bloodgroup="B+"),
        'B2':blood_models.Stock.objects.get(bloodgroup="B-"),
        'AB1':blood_models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':blood_models.Stock.objects.get(bloodgroup="AB-"),
        'O1':blood_models.Stock.objects.get(bloodgroup="O+"),
        'O2':blood_models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=blood_forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=blood_models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'hod_templates/admin_blood.html',context=dict)

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()
    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    donorscount=donor_models.Donor.objects.all().count()
    totalunit=blood_models.Stock.objects.aggregate(Sum('unit'))
    totalbloodunit=totalunit['unit__sum']
    totalrequest=blood_models.BloodRequest.objects.all().count()
    totalapprovedrequest=blood_models.BloodRequest.objects.all().filter(status='Approved').count()
    requests_=blood_models.BloodRequest.objects.all().filter(status='Pending').count()

    total_donations=donor_models.BloodDonate.objects.filter(status="Approved").count()
    donation_approval=donor_models.BloodDonate.objects.filter(status="Pending").count()


    print(total_donations)

    today = datetime.today()
    for_today = models.Patient.objects.filter(admitDate__year=today.year, admitDate__month=today.month, admitDate__day=today.day).count()
    print(for_today)
    
    doctors=0
    pharmacist=0
    receptionist=0
    out_of_stock=0
    total_stock=0
    
    for_today = 0
    
    exipred=0
     

    context={
        "all_doctors":doctorcount,
        "pendingdoctorcount":pendingdoctorcount,
        "patientcount":patientcount,
        'pendingpatientcount':pendingpatientcount,
        "appointmentcount":appointmentcount,
        "pendingappointmentcount":pendingappointmentcount,
        "donorscount":donorscount,
        "totalrequest":totalrequest,
        "totalapprovedrequest":totalapprovedrequest,
        "totalbloodunit":totalbloodunit,
        "for_today":for_today,
        "total_donations":total_donations,
        "donation_approval":donation_approval,
        "requests_":requests_,
     

        "expired_total":exipred,
        "out_of_stock":out_of_stock,
        "total_drugs":total_stock,

        

        "all_pharmacists":pharmacist,
        "all_clerks":receptionist,

    }

 
    return render(request,'hod_templates/admin_dashboard.html',context)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    staffs=models.Doctor.objects.all().filter(status=True)

    context = {
        "staffs": staffs,
        "title":"Dotors Details"
    }

    return render(request,'hod_templates/manage_doctor.html',context)






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        try:
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                doctor=doctorForm.save(commit=False)
                doctor.status=True
                doctor.save()
                messages.success(request, "Staff Updated Successfully.")
                return redirect('admin-view-doctor')
        except:
            messages.success(request, "error while updating")
    return render(request,'hod_templates/edit_doctor.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        try:
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()

                doctor=doctorForm.save(commit=False)
                doctor.user=user
                doctor.status=True
                doctor.save()

                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                messages.success(request, "Doctor Added Successfully!")

            return HttpResponseRedirect('admin-view-doctor')
        except:
            messages.error(request, "Failed to Add Doctor!")
            return HttpResponseRedirect('admin-view-doctor')

    return render(request,'hod_templates/edit_doctor.html',context=mydict)








@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hod_templates/approve_doctor.html',{'doctors':doctors})





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_history(request):
    doctors=models.Doctor.objects.all()
    return render(request,'hod_templates/view_doctor.html',{'doctors':doctors})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-view-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    messages.success(request, "Doctor Deleted!")

    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hod_templates/specialisation.html',{'doctors':doctors})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hod_templates/admited_patients.html',{'patients':patients})






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            messages.success(request, "Patient Updated Successfully!")

            return redirect('admin-view-patient')
    return render(request,'hod_templates/edit_patient.html',context=mydict)


def patient_personalRecords(request,pk):
    patient=models.Patient.objects.get(id=pk)
    # prescrip=patient.prescription_set.all()
    # stocks=patient.dispense_set.all()

    context={
        "patient":patient,
        # "prescription":prescrip,
        # "stocks":stocks

    }
    return render(request,'hod_templates/patient_personalRecords.html',context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request, "Patient Added Successfully!")


        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hod_templates/patient_form.html',context=mydict)







#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hod_templates/approve_patients.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    messages.success(request, "Patient Added Successfully!")
    return redirect(reverse('admin-view-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):

    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    messages.success(request, "Patient Rejected!")

    return redirect('admin-view-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hod_templates/discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hod_templates/bill.html',context=patientDict)
    return render(request,'hod_templates/bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hod_templates/appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hod_templates/book_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hod_templates/approve_appointments.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    messages.success(request, "Appointment Confirmed!")
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    messages.success(request, "Appointment Rejected!")
    return redirect('admin-approve-appointment')






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def createPharmacist(request):
    userForm=forms.PharmacistUserForm()
    PharmacistForm=forms.PharmacistForm()
    mydict={'userForm':userForm,'PharmacistForm':PharmacistForm}
    if request.method=='POST':
        userForm=forms.PharmacistUserForm(request.POST)
        PharmacistForm=forms.PharmacistForm(request.POST, request.FILES)
        if userForm.is_valid() and PharmacistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            Pharmacist=PharmacistForm.save(commit=False)
            Pharmacist.user=user
            Pharmacist=Pharmacist.save()
            my_Pharmacist_group = Group.objects.get_or_create(name='Pharmacist')
            my_Pharmacist_group[0].user_set.add(user)

        return redirect('admin-dashboard')
    
    return render(request,'hod_templates/pharmacist_form.html',context=mydict)



def managePharmacist(request):
    staffs = models.Pharmacist.objects.all()
    print(staffs)
    context = {
        "staffs": staffs,
        "title":"Manage Pharmacist"
    }

    return render(request,'hod_templates/all_pharmacist.html',context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def editPharmacist(request,pk):
    Pharmacist=models.Pharmacist.objects.get(id=pk)
    user=models.User.objects.get(id=Pharmacist.user_id)
    userForm=forms.PharmacistUserForm(instance=user)
    PharmacistForm=forms.PharmacistForm(request.FILES,instance=Pharmacist)
    mydict={'userForm':userForm,'PharmacistForm':PharmacistForm}
    if request.method=='POST':
        userForm=forms.PharmacistUserForm(request.POST,instance=user)
        PharmacistForm=forms.PharmacistForm(request.POST,request.FILES,instance=Pharmacist)
        try:
            if userForm.is_valid() and PharmacistForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                Pharmacist=PharmacistForm.save(commit=False)
                Pharmacist.user=user
                Pharmacist=Pharmacist.save()
                messages.success(request, " Updated Successfully.")
                return redirect('manage_pharmacist')
        except:
            messages.success(request, "error while updating")
    return render(request,'hod_templates/edit_pharmacist.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deletePharmacist(request,pk):
    Pharmacist=models.Pharmacist.objects.get(id=pk)
    user=models.User.objects.get(id=Pharmacist.user_id)
    user.delete()
    Pharmacist.delete()
    messages.success(request, "Pharmacist Deleted!")
    return redirect('manage_pharmacist')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addStock(request):
    form=forms.StockForm(request.POST,request.FILES)
    if form.is_valid():
        form=forms.StockForm(request.POST,request.FILES)
        form.save()
        return redirect('add_stock')
    context={
        "form":form,
        "title":"Add New Drug"
    }
    return render(request,'hod_templates/add_stock.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def manageStock(request):
    stocks = models.Stock.objects.all().order_by("-id")
    ex=models.Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo=models.Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    context = {
        "stocks": stocks,
        "expired":ex,
        "expa":eo,
        "title":"Manage Stocked Drugs"
    }
    return render(request,'hod_templates/manage_stock.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addCategory(request):
    try:
        form=forms.CategoryForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")
                return redirect('add_category')
    except:
        messages.error(request, "Category Not added! Try again")
        return redirect('add_category')
    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    return render(request,'hod_templates/add_category.html',context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addPrescription(request):
    form=forms.PrescriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('prescribe')
    context={
        "form":form,
        "title":"Prescribe Drug"
    }
    return render(request,'hod_templates/prescribe.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reorder_level(request, pk):
    queryset = models.Stock.objects.get(id=pk)
    form = forms.ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.drug_name) + " is updated to " + str(instance.reorder_level))
        return redirect("manage_stock")
    context ={
        "instance": queryset,
        "form": form,
        "title":"Reorder Level"
    }
    return render(request,'hod_templates/reorder_level.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def editStock(request,pk):
    drugs=models.Stock.objects.get(id=pk)
    form=forms.StockForm(request.POST or None,instance=drugs)
    if request.method == "POST":
        if form.is_valid():
            form=forms.StockForm(request.POST or None ,instance=drugs)
            category=request.POST.get('category')
            drug_name=request.POST.get('drug_name')
            quantity=request.POST.get('quantity')
            try:
                drugs =models.Stock.objects.get(id=pk)
                drugs.drug_name=drug_name
                drugs.quantity=quantity
                drugs.save()
                form.save()
                messages.success(request,'Receptionist Updated Succefully')
            except:
                messages.error(request,'An Error Was Encounterd Receptionist Not Updated')
    context={
        "drugs":drugs,
         "form":form,
         "title":"Edit Stock"

    }
    return render(request,'hod_templates/edit_drug.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deleteDrug(request,pk):
    try:
        drugs=models.Stock.objects.get(id=pk)
        if request.method == 'POST':
            drugs.delete()
            messages.success(request, "Pharmacist  deleted successfully")      
            return redirect('manage_stock')
    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect('manage_stock')
    return render(request,'hod_templates/sure_delete.html')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def drugDetails(request,pk):
    stocks=models.Stock.objects.get(id=pk)
    context={
        "stocks":stocks,
    }
    return render(request,'hod_templates/view_drug.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def receiveDrug(request,pk):
    receive=models.Stock.objects.get(id=pk)
    form=forms.ReceiveStockForm()
    try:
        form=forms.ReceiveStockForm(request.POST or None )
        if form.is_valid():
            form=forms.ReceiveStockForm(request.POST or None ,instance=receive)
            instance=form.save(commit=False) 
            instance.quantity+=instance.receive_quantity
            instance.save()
            form=forms.ReceiveStockForm()
            messages.success(request, str(instance.receive_quantity) + " " + instance.drug_name +" "+ "drugs added successfully")
            return redirect('manage_stock')
    except:
        messages.error(request,"An Error occured, Drug quantity Not added")    
        return redirect('manage_stock')
    context={
            "form":form,
            "title":"Add Drug"
        }
    return render(request,'hod_templates/modal_form.html',context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def patient_feedback_message(request):
    feedbacks = models.PatientFeedback.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_templates/patient_feedback.html', context)

@csrf_exempt
def patient_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')
    try:
        feedback =  models.PatientFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def addPrescription2(request,pk):        
    patient=models.Patient.objects.get(id=pk)
    form=forms.PrescriptionForm(initial={'patient_id':patient})
    try:
        form=forms.PrescriptionForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'Prescription added successfully')
            return redirect('doctor-view-patient')
    except:
        messages.error(request,'Prescription Not Added')
        return redirect('doctor-view-patient')

    context={
            "form":form
        }
    return render(request,'hospital/doctor_manage_prescription.html',context)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def patient_personalDetails(request,pk):
    patient=models.Patient.objects.get(id=pk)
    prescrip=patient.prescription_set.all()
    print(prescrip)

    context={
        "patient":patient,
        "prescription":prescrip

    }
    return render(request,'hospital/patient_personalRecords.html',context)

   
    
#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_feedback(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    feedback = models.PatientFeedback.objects.filter(patient_id=patient)
    context = {
        "feedback":feedback
    }
    return render(request, "hospital/patient_feedback.html", context)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_feedback_save(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback_message')
        staff_obj = models.Patient.objects.get(user_id=request.user.id)
        add_feedback =models.PatientFeedback(patient_id=staff_obj, feedback=feedback, feedback_reply="")
        add_feedback.save()
        messages.success(request, "Feedback Sent.")
        return redirect('patient_feedback')

#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



