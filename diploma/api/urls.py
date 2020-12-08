from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from diploma.api.app_urls import urls

app_name = 'api'

urlpatterns = [
	path('domestic_services/', include(urls.urlpatterns))
]
