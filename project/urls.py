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

    path('mfa/(?P<sesion>\d+)/$', pg_view.mfa, name='mfa'),

    path('menu/(?P<sesion>\d+)(?P<rol>\d+)$', pg_view.menu, name='menu'),

    path('crearPlanEstudios/(?P<sesion>\d+)/$', pg_view.crearPlanEstudios, name='crearPlanEstudios'),

    path('mostrarPlanEstudios/(?P<sesion>\d+)/$', pg_view.mostrarPlanEstudios, name='mostrarPlanEstudios'),

    path('mostrarPlanEstudiosDetalle/(?P<sesion>\d+)(?P<idplan>\d+)/$', pg_view.mostrarPlanEstudiosDetalle, name='mostrarPlanEstudiosDetalle'),

    path('crearMateria/(?P<sesion>\d+)/$', pg_view.crearMateria, name='crearMateria'),

    path('agregarMateria/(?P<sesion>\d+)(?P<idplan>\d+)/$', pg_view.agregarMateria, name='agregarMateria'),

    path('mostrarMaterias/(?P<sesion>\d+)/$', pg_view.mostrarMaterias, name='mostrarMaterias'),

    path('mostrarMateriaDetalle/(?P<sesion>\d+)(?P<idmateria>\d+)/$', pg_view.mostrarMateriaDetalle,
         name='mostrarMateriaDetalle'),

    path('crearContenidoCurricular/(?P<sesion>\d+)(?P<idmateria>\d+)/$', pg_view.crearContenidoCurricular, name='crearContenidoCurricular'),

    path('mostrarContenidoCurricular/(?P<sesion>\d+)(?P<idcontenidocurricular>\d+)(?P<idmateria>\d+)(?P<descriptor>\d+)/$',
         pg_view.mostrarContenidoCurricular, name='mostrarContenidoCurricular'),

    path('mostrarUnidad/(?P<sesion>\d+)(?P<idunidad>\d+)/$',
        pg_view.mostrarUnidad, name='mostrarUnidad'),

    path('mostrarActFormacionPractica/(?P<sesion>\d+)(?P<idactformacionpractica>\d+)/$',
        pg_view.mostrarActFormacionPractica, name='mostrarActFormacionPractica'),

    path('crearCompetencia/(?P<sesion>\d+)(?P<idplan>\d+)/$', pg_view.crearCompetencia, name='crearCompetencia'),

    path('mostrarCompetencias/(?P<sesion>\d+)/$', pg_view.mostrarCompetencias, name='mostrarCompetencias'),

    path('mostrarCompetenciaDetalle/(?P<sesion>\d+)(?P<idcompetencia>\d+)/$', pg_view.mostrarCompetenciaDetalle,
         name='mostrarCompetenciaDetalle'),

    path('crearCapacidad/(?P<sesion>\d+)(?P<idcompetencia>\d+)/$', pg_view.crearCapacidad, name='crearCapacidad'),

    path('crearUnidad/(?P<sesion>\d+)(?P<idcontenidocurricular>\d+)/$', pg_view.crearUnidad, name='crearUnidad'),

    path('crearActa/(?P<sesion>\d+)(?P<idcontenidocurricular>\d+)/$', pg_view.crearActa, name='crearActa'),
]
