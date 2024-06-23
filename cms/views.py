from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import  generics
from django.contrib.auth import get_user_model
from .serializers import UserLoginSerializer, UploadFileSerializer, UserSignupSerializer
from.models import  UploadFile
from django.conf import settings
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
import smtplib, ssl
from rest_framework_simplejwt.views import TokenObtainPairView
from .token import CustomTokenSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOpsUser, IsClientUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.signing import TimestampSigner
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
import os
import send_mail

User = get_user_model()
# Create your views here.


class LoginViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            try:
                 userdata = User.objects.get(username=user["username"],password =user["password"])
                 refresh = CustomTokenSerializer.get_token(userdata)
                 return Response({
                     'refresh': str(refresh),
                      'access': str(refresh.access_token),
                 })
            except  User.DoesNotExist:
                 return Response({"message": "Login successful"})
    

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes =[AllowAny]


    def send_test_email(request):
        send_mail(
          'Test Email Subject',
          'This is a test email body.',
          'webmaster@localhost',  # This should match DEFAULT_FROM_EMAIL
          ['recipient@example.com'],  # Replace with the recipient's email address
        fail_silently=False,
         )
        return HttpResponse('Test email sent successfully.')

class FileUploadView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsOpsUser]
    def put(self,request):
        file = request.data.get('file')
        if not file.name.endswith(('.pptx','.docx','.xlsx','.pdf')): 
            return Response({"error":"Invalid file type"})
        else:
            fs = FileSystemStorage()
            name = fs.save(file.name,file)
            data=UploadFile(type=name.split(".")[1],filename=name)
            data.save()
            return Response("Uploaded sucessfully ")
        
class DownloadFileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]
    def get(self,request):
        try:
            file_id=request.query_params.get("file_name")
            signer = TimestampSigner()

            # Generate a signed value for the file_id
            signed_value = signer.sign(file_id)
            encoded_value = urlsafe_base64_encode(force_bytes(signed_value))
            # Generate a secure URL
            secure_url = f"{request.build_absolute_uri('/api/cms/download/')}?file={encoded_value}"
            return Response({"secure_url": secure_url}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class DownloadFileThroughLink(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsClientUser]
    def get(self,request):
        file = request.query_params.get('file')

        if not file:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            signer = TimestampSigner()
            decoded_value = force_str(urlsafe_base64_decode(file))
            original_value = signer.unsign(decoded_value, max_age=3600)  # The link is valid for 1 hour
            print(original_value)
            # Get the file path from the UploadedFile model
            try:
                fs = FileSystemStorage()
                file=fs.open(original_value)
            except UploadFile.DoesNotExist:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

           
            response = HttpResponse(FileWrapper(file), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(original_value)}"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ListFileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]
    def get(self,request):
       files = [file.filename for file in UploadFile.objects.all()] 
       return Response(files)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer      






