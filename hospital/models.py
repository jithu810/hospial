from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='static/profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"



class Pharmacist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='static/profile_pic/Pharmacist/',null=True,blank=True,default = None)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    



class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)
    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)



class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return str(self.name)

    
class Prescription(models.Model):
    patient_id = models.ForeignKey(Patient,null=True, on_delete=models.SET_NULL)
    description=models.TextField(null=True)
    prescribe=models.CharField(max_length=100,null=True)
    date_precribed=models.DateTimeField(auto_now_add=True, auto_now=False)



class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )

class Stock(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE,blank=True)
    drug_imprint=models.CharField(max_length=6 ,blank=True, null=True)
    drug_name = models.CharField(max_length=50, blank=True, null=True)
    drug_color = models.CharField(max_length=50, blank=True, null=True)
    drug_shape = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    manufacture= models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    drug_strength= models.CharField(max_length=10, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True,default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_description=models.TextField(blank=True,max_length=1000,null=True)
    drug_pic=models.ImageField(default="images2.png",null=True,blank=True)
    objects = ExpiredManager()
   
    def __str__(self):
        return str(self.drug_name)

 
class Dispense(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING,null=True)
    drug_id = models.ForeignKey(Stock, on_delete=models.SET_NULL,null=True,blank=False)
    dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
    taken=models.CharField(max_length=300,null=True, blank=True)
    stock_ref_no=models.CharField(max_length=300,null=True, blank=True)
    instructions=models.TextField(max_length=300,null=True, blank=False)
    dispense_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)


class PatientFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    pharmacist_id=models.ForeignKey( Pharmacist,null=True, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)
    feedback_reply = models.TextField(null=True)
    admin_created_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()