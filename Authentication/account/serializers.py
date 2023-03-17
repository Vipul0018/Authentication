from rest_framework import serializers
from account.models import User
from account.utils import Util
from django.core.mail import send_mail

from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegisterSrializer(serializers.ModelSerializer):
     # we write this becz we need confirm password field our registatin request
     password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
       
     class Meta:
        model = User
        fields =  ['name','email','tc','password','password2']
        extra_kwargs ={
            'password':{'write_only':True}
        }

     # pass and confirm pass validate
     def validate(self, attrs):
         password = attrs.get('password')
         password2 = attrs.get('password2')
         if password != password2:
             raise serializers.ValidationError("password and confirm password does not match")
         return attrs
     # create method using create user modelserializer mai built hota hai lekin humne modle costom banya hai
     def create(self,validate_data):
         return User.objects.create_user(**validate_data)
     

class UseLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChagePassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user = self.context.get('user') # context ko access kiya
        if password != password2:
            raise serializers.ValidationError("password and confirm password doenot match")
        user.set_password(password)
        user.save()
        return attrs
    


class SendEmailResetPassSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user =  User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/auth/api/reset/'+uid+'/'+token
            

        # ==========================EMAIL===================================#            #Send Email
            
            body = 'Click following link to reset your password '+link
            data={
                'subject':'Rest Your Password',
                'body':body,
                'to_email':user.email
 
            }
            Util.send_email(data)

        # ==========================EMAIL===================================#            print("link : ",link)
            return attrs 
            
        else:
            raise ValueError("You are not register user")
class UserPassResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid = self.context.get('uid') # context ko access kiya
            token = self.context.get('token') # context ko access kiya
            if password != password2:
                raise serializers.ValidationError("password and confirm password doenot match")
            id = smart_str(urlsafe_base64_decode(uid))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValueError("Token is not valid it Expire ")
            user.set_password(password)
            user.save()
            
            return attrs

        except DjangoUnicodeDecodeError as identifier :
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValueError("Token is not valid it Expire ")

