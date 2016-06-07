from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^mine/$', views.ManageCourseListView.as_view(), name="manage_course_list"),
    url(r'^create/$', views.CourseCreateView.as_view(), name="course_create"),
    url(r'^(?P<pk>\d+)/edit/$', views.CourseUpdateView.as_view(), name="course_edit"),
    url(r'^(?P<pk>\d+)/delete/$',
        views.CourseDeleteView.as_view(), name="course_delete"),

    # управление модулями курса
    url(r'^(?P<pk>\d+)/module/$', views.CourseModuleUpdateView.as_view(),
        name="course_module_update"),

    # создание контента
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/create/$',
        views.ContentCreateUpdateView.as_view(),
        name="module_content_create"),
    # обновление контента
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$',
        views.ContentCreateUpdateView.as_view(),
        name="module_content_update"),
    # удаление контента
    url(r'^content/(?P<id>\d+)/delete/$',
        views.ContentDeleteView.as_view(),
        name="module_content_delete"),

    # отображение списка контента модуля
    url(r'^module/(?P<module_id>\d+)/$',
        views.ModuleContentListView.as_view(),
        name="module_content_list"),

    # сортировка модулей
    url(r'^module/order/$', views.ModuleOrderView.as_view(), name="order_modules"),
    # сортировка контента
    url(r'^content/order/$', views.ContentOrderView.as_view(), name="order_contents"),

    url(r'^subject/(?P<subject>[\w-]+)/$', views.CourseListView.as_view(), name="course_list_subject"),
    url(r'^(?P<slug>[\w-]+)/$', views.CourseDetailView.as_view(), name="course_detail"),
]
