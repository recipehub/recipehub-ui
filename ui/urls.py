from django.conf import settings
from django.contrib import admin, auth
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from recipehub.views import RecipeListCreateView, RecipeDetailView, CommentListCreateView, RatingCreateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/recipe/(?P<recipe_id>[0-9]+)/$', RecipeDetailView.as_view()),
    url(r'^api/v1/recipe/$', RecipeListCreateView.as_view()),
    url(r'^api/v1/comment/$', CommentListCreateView.as_view()),
    url(r'^api/v1/rating/$', RatingCreateView.as_view()),
    url(r'', TemplateView.as_view(template_name='index.html')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]

# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += patterns('',
#             url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )
