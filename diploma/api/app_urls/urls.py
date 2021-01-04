from django.urls import path, include
from diploma.api.app_urls import authentification, work, order, answer, black_list, reaction

app_name = 'app_urls'
urlpatterns = [
	path('authentification/', include(authentification.urlpatterns)),
	path('work/', include(work.urlpatterns)),
	path('order/', include(order.urlpatterns)),
	path('answer/', include(answer.urlpatterns)),
	path('black_list/', include(black_list.urlpatterns)),
	path('reaction/', include(reaction.urlpatterns)),
]
