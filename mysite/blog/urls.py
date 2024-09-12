from django.urls import path
from .views import home_page, register_page, login_page, personal_page_view, race_page_view, reff_page_view, register_result_view
# from .views import LoginAPIView

urlpatterns = [
    path('', home_page, name='home_page'),  # 首頁路徑
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('personal/<int:player_id>/', personal_page_view, name='personal_page'),
    path('race/<int:player_id>/', race_page_view, name='race_page'),  # 传递 player_id
    path('reff/', reff_page_view, name='reff_page'),  # 配置裁判页面的路由
    path('register_result/<int:match_id>/', register_result_view, name='register_result'),
 
]