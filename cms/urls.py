
from django.urls import path,include
from .views import LoginViews,FileUploadView,  SignupView,DownloadFileView,DownloadFileThroughLink,  ListFileView,MyTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [
    path ('login/',LoginViews.as_view(), name='login'),
    path('upload_file/',FileUploadView.as_view(),name = 'upload_file'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('download-link/', DownloadFileView.as_view(), name = 'download-link'),
    path('download/', DownloadFileThroughLink.as_view(), name = 'download'),
    path('files/', ListFileView.as_view(), name= 'files'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
 

if settings.DEBUG:
    urlpatterns == static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)