
from django.contrib import admin
from django.urls import path, include
from pg import views as pg_view
from django.contrib.auth import views as auth


urlpatterns = [

    path('admin/', admin.site.urls),

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

    path('crearMateria/(?P<nombre>\d+)/$', pg_view.crearMateria, name='crearMateria'),

    path('mostrarMaterias/(?P<nombre>\d+)/$', pg_view.mostrarMaterias, name='mostrarMaterias'),

    path('mostrarMateriaDetalle/(?P<nombre>\d+)(?P<idmateria>\d+)/$', pg_view.mostrarMateriaDetalle,
         name='mostrarMateriaDetalle'),

    path('crearContenidoCurricular/(?P<nombre>\d+)(?P<idmateria>\d+)/$', pg_view.crearContenidoCurricular, name='crearContenidoCurricular'),

    path('mostrarContenidoCurricular/(?P<nombre>\d+)(?P<idcontenidocurricular>\d+)(?P<idmateria>\d+)(?P<descriptor>\d+)/$',
         pg_view.mostrarContenidoCurricular, name='mostrarContenidoCurricular'),

    path('mostrarUnidad/(?P<nombre>\d+)(?P<idunidad>\d+)/$',
        pg_view.mostrarUnidad, name='mostrarUnidad'),

    path('mostrarActFormacionPractica/(?P<nombre>\d+)(?P<idactformacionpractica>\d+)/$',
        pg_view.mostrarActFormacionPractica, name='mostrarActFormacionPractica'),

    path('crearCompetencia/(?P<nombre>\d+)(?P<idplan>\d+)/$', pg_view.crearCompetencia, name='crearCompetencia'),

    path('mostrarCompetencias/(?P<nombre>\d+)/$', pg_view.mostrarCompetencias, name='mostrarCompetencias'),



]
