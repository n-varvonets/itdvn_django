from django.urls import path
from lesson_8 import views

urlpatterns = [
    path('upload/', views.upload_data, name='upload'),
    path('filter/', views.FilterGameView.as_view(), name='filter'),
    # path('relation-filter/', views.relation_filter_view,
    #      name='relation_filter'),
    path('exclude/', views.ExcludeGameView.as_view(), name='exclude'),
    path('orderby/', views.OrderedByView.as_view(), name='orderby'),
    path('all/', views.AllView.as_view(), name='all'),
    path('union/', views.UnionView.as_view(), name='union'),
    path('none/', views.NoneView.as_view(), name='none'),
    path('values/', views.ValuesView.as_view(), name='values'),
    path('dates/', views.date_view, name='dates'),
    # path('get/', views.get_view, name='get'),
    # path('create/', views.create_view, name='create'),
]
