from django.urls import path, include
from diploma.api.app_urls import authentification, work

app_name = 'app_urls'
urlpatterns = [
	path('authentification/', include(authentification.urlpatterns)),
	path('work/', include(work.urlpatterns)),
]
