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
from django.core.mail import send_mail

User = get_user_model()
# Create your views here.


class LoginViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request):
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
                 return Response({"message": "Error in login"})
    

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes =[AllowAny]
    
    def post(self,request):
            email= request.data["email"]
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                data=User(username= user['username'], password= user['password'], email= user['email'], user_type= user['user_type'])
                data.save()
            send_mail(
             'Email Verifiation Mail',
             f'Dear ${email}\n This mail is to verify your email id',
             'cms@localhost',  
             [email],
             fail_silently=False,
            )
            return HttpResponse('User registered successfully, verification email sent successfully.')



class FileUploadView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsOpsUser]
    def post(self,request):
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
            signed_value = signer.sign(file_id)
            encoded_value = urlsafe_base64_encode(force_bytes(signed_value))
            secure_url = f"{request.build_absolute_uri('/api/cms/download/')}?file={encoded_value}"
            return Response({"download-link": secure_url,"message":"success"}, status=status.HTTP_200_OK)

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
            original_value = signer.unsign(decoded_value) 
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
