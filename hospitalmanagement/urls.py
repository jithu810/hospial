


from django.contrib import admin
from django.urls import path,include
from hospital import views

from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('admin_doctor_history', views.admin_doctor_history,name='admin_doctor_history'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),

]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]


#---------FOR Donor RELATED URLS-------------------------------------
urlpatterns +=[
path('donor/',include('donor.urls')),

path('admin-donor', views.admin_donor_view,name='admin-donor'),
path('update-donor/<int:pk>', views.update_donor_view,name='update-donor'),
path('delete-donor/<int:pk>', views.delete_donor_view,name='delete-donor'),

path('admin-request', views.admin_request_view,name='admin-request'),



path('admin_donation_history', views.admin_donation_history,name='admin_donation_history'),
path('admin-donation', views.admin_donation_view,name='admin-donation'),
path('approve-donation/<int:pk>', views.approve_donation_view,name='approve-donation'),
path('reject-donation/<int:pk>', views.reject_donation_view,name='reject-donation'),



path('admin-request-history', views.admin_request_history_view,name='admin-request-history'),
path('update-approve-status/<int:pk>', views.update_approve_status_view,name='update-approve-status'),
path('update-reject-status/<int:pk>', views.update_reject_status_view,name='update-reject-status'),

path('admin-blood', views.admin_blood_view,name='admin-blood'),


]

#---------FOR Admin RELATED URLS-------------------------------------
urlpatterns +=[
    path('admin_edit_doctor/<int:pk>/', views.update_doctor_view, name="admin_edit_doctor"),
    path('patient_personalRecords/<pk>/',views.patient_personalRecords,name='patient_record'),
    path('add_pharmacist/',views.createPharmacist,name='add_pharmacist'),

    path('manage_pharmacist/',views.managePharmacist,name='manage_pharmacist'),
    path('edit_pharmacist/<int:pk>/', views.editPharmacist, name="edit_pharmacist"),
    path('delete_pharmacist/<str:pk>/',views.deletePharmacist,name='delete_pharmacist'),

    path('add_stock/',views.addStock,name='add_stock'),
    path('add_category/',views.addCategory,name='add_category'),
    path('manage_stock/',views.manageStock,name='manage_stock'),    
    path('prescribe_drug/',views.addPrescription,name='prescribe'),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('edit_drug/<pk>/', views.editStock, name="edit_drug"),
    path('delete_drug/<str:pk>/',views.deleteDrug,name='delete_drug'),
    path('drug_details/<str:pk>/', views.drugDetails, name="drug_detail"),
    path('receive_drug/<pk>/', views.receiveDrug, name="receive_drug"),

    path('doctor_prescribe_drug/<str:pk>/',views.addPrescription2,name='doctor_prescribe_drug'),
    path('patient_personalDetails/<str:pk>/',views.patient_personalDetails,name='patient_record_doctor'),
    path('patient_feedback/',views.patient_feedback,name='patient_feedback'),
    path('staff_feedback_save/', views.patient_feedback_save, name="patient_feedback_save"),

path('patient_feedback_message/', views.patient_feedback_message, name="patient_feedback_message"),
path('patient_feedback_message_reply/', views.patient_feedback_message_reply, name="patient_feedback_message_reply"),

]