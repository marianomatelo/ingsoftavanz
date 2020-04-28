
from django.contrib import admin
from django.urls import path, include
from pg import views as pg_view
from django.contrib.auth import views as auth


urlpatterns = [

    path('admin/', admin.site.urls),

    #####pg related path##########################
    path('', include('pg.urls')),
    path('login/', pg_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='pg/index.html'), name='logout'),
    # path('register/', pg_view.register, name='register'),

    path('/', pg_view.index, name='index'),

    path('mfa/(?P<nombre>\d+)/$', pg_view.mfa, name='mfa'),

    path('menu/(?P<nombre>\d+)/$', pg_view.menu, name='menu'),

    path('crearPlanEstudios/(?P<nombre>\d+)/$', pg_view.crearPlanEstudios, name='crearPlanEstudios'),

    path('mostrarPlanEstudios/(?P<nombre>\d+)/$', pg_view.mostrarPlanEstudios, name='mostrarPlanEstudios'),

    path('mostrarPlanEstudiosDetalle/(?P<nombre>\d+)(?P<idplan>\d+)/$', pg_view.mostrarPlanEstudiosDetalle, name='mostrarPlanEstudiosDetalle'),

    # path('datasets/', pg_view.dataset, name='datasets'),
    #
    # path('playground/', pg_view.playground, name='playground'),
    #
    # path('analyzer/', pg_view.analyzer, name='analyzer'),

]
