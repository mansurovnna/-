from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('', include('catalog.urls')),
    path('postuser/', views.postuser),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
