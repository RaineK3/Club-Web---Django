from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    #to deal with member authentication
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#configure admin titles
admin.site.site_header = "My Club Adminstration Page"
admin.site.site_title = "My Club"
admin.site.index_title = "Welcome to the admin area..."