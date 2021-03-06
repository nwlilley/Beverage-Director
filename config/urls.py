
from django.contrib import admin
from bevdir import views
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', views.welcome_page, name='welcome-page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/profile/', views.homepage, name='homepage'),
    path('api/', include('bevdir.urls')),
    path('drinkbuilder/', views.drink_builder, name='drink-builder'),
    path('cocktails/<int:pk>/', views.edit_cocktail, name='edit-cocktail')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
