from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from recipehub.views import RecipeListCreateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mylogin/', TemplateView.as_view(template_name='login.html')),
    url(r'^api/v1/recipe/', RecipeListCreateView.as_view()),
    url(r'', TemplateView.as_view(template_name='index.html')),
    url('', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
