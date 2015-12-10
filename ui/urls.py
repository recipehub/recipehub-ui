from django.conf import settings
from django.contrib import admin, auth
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from recipehub.views import RecipeListCreateView, RecipeDetailView, CommentListCreateView, RatingCreateView, current_user, ForkListCreateView, VersionListView, RecipeImageGetCreateView, IngredientListView, search


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/comment/$', CommentListCreateView.as_view()),
    url(r'^api/v1/user/$', current_user),
    url(r'^api/v1/search/$', search),
    url(r'^api/v1/rating/$', RatingCreateView.as_view()),
    url(r'^api/v1/recipe/(?P<recipe_id>[0-9]+)/$', RecipeDetailView.as_view()),
    url(r'^api/v1/version/(?P<recipe_id>[0-9]+)/$', VersionListView.as_view()),
    url(r'^api/v1/recipe/$', RecipeListCreateView.as_view()),
    url(r'^api/v1/image/$', RecipeImageGetCreateView.as_view()),
    url(r'^api/v1/ingredient/$', IngredientListView.as_view()),
    url(r'^api/v1/fork/$', ForkListCreateView.as_view()),
    url(r'', include('django.contrib.auth.urls', namespace='auth')),
    url(r'', TemplateView.as_view(template_name='index.html')),
]

# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += patterns('',
#             url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )
