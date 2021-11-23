from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ShowHomeView.as_view(), name='home'),
    path('report/', views.ShowReportView.as_view(), name='report-view'),
    path('report/<str:username>/', views.ShowUserReportView.as_view(), name='user-reports'),
    path('report-add/', views.report_update, name='report-add'),
    path('tarifs-add/', views.CreateTarifsView.as_view(), name='tarifs-add'),
    path('tarifs-show/', views.ShowUserTarifsView.as_view(), name='tarifs-show'),
    path('report/<int:pk>/update/', views.UpdateReportView.as_view(), name='report-update'),
    path('rating/view/', views.InputRatingView.as_view(), name='rating-view'),
    path('check-in/', views.CreateCheckView.as_view(), name='check-in'),
    # path('check-in/', views.create_post, name='check-in'),
    path('check-show/', views.ShowCheckView.as_view(), name='check-show'),
    path('ajax/', views.chart_area, name='chart-area'),
    path('map/', views.map, name='map'),
    path('rating-input', views.rating_input, name='rating-input'),
    path('saverating', views.saverating, name='saverating'),
    path('savecheck', views.savecheck, name='savecheck'),
    path('super-timetable/', views.ShowSuperTimetableView.as_view(), name='super-timetable'),
]