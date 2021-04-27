from django.urls import path

from diploma.apps.verification.views import RequestForCode, VerifyCode

urlpatterns = [
	path('request_code/', RequestForCode.as_view(), name='request_code'),
	path('verify_code/', VerifyCode.as_view(), name='verify_code'),
]
