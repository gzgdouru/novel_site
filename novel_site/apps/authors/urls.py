from django.conf.urls import url

from .views import AuthorsListView, AuthorsDetailView

app_name = "authors"

urlpatterns = [
    url(r'^list/$', AuthorsListView.as_view(), name="authors_list"),
    url(r'^detail/(?P<author_id>\d+)/$', AuthorsDetailView.as_view(), name="authors_detail"),
]