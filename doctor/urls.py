from django.urls import path

from doctor import views 

app_name="doctor"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name="appointments"),

     path("appointments/<appointment_id>/", views.appointment_detail, name="appointment_detail"),


    path("cancel_appointment/<appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    
    path("activate_appointment/<appointment_id>/", views.activate_appointment, name="activate_appointment"),
    
    path("complete_appointment/<appointment_id>/", views.complete_appointment, name="complete_appointment"),

    #medikal rapor url konfigrasyonu
    path("add_medical_report/<appointment_id>/", views.add_medical_report, name ="add_medical_report"),

    path("edit_medical_report/<appointment_id>/<medical_report_id>/", views.edit_medical_report, name ="edit_medical_report"),

    #laboratuvar rapor url konfigrasyonu
    path("add_lab_test/<appointment_id>/", views.add_lab_test, name="add_lab_test"),
    path("edit_lab_test/<appointment_id>/<lab_test_id>/", views.edit_lab_test, name="edit_lab_test"),

    #reçete url kongfirasyonu
    path("add_prescription/<appointment_id>/", views.add_prescription, name="add_prescription"),
    path("edit_prescription/<appointment_id>/<prescription_id>/", views.edit_prescription, name="edit_prescription"),

    #ödeme bilgisi url konfigrasyonu
    path("payments/", views.payments, name="payments"),

    #doktor bildirimleri
    path("notifications/", views.notifications, name="notifications"),
    path("mark_noti_seen/<id>/", views.mark_noti_seen, name="mark_noti_seen"),

    #doktor profili düzenleme
    path("profile/", views.profile, name="profile"),

]
