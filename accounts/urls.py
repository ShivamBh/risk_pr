from django.conf.urls import url
from .views import index,tokenurl

urlpatterns = [
	 url(r'^$', index, name='home'),
	 url('generatetokenurl', tokenurl, name='generatetokenurl'),
	
]
