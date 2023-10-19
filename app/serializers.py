
from rest_framework import serializers
from app.models import NewUser,TodoModel
import re
import datetime



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id','name','email','password','password2')
        
    def validate_email(self,email):      
        if not  re.search("^[a-zA-Z0-9+_.]+@[a-zA-Z0-9.]+$",email):
            raise serializers.ValidationError('email not validate')
        return email
        
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password not same') 
        return attrs
    
    def create(self, validate_data):
        return NewUser.objects.create(**validate_data)
    
    

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email','password')
        
    
class TaskSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = TodoModel
        fields = ('id','email','taskname','comments','status','date')
        
        read_only_fields  = ('taskname','date','email',)
            
        def create(self, validate_data):
             return TodoModel.objects.create(**validate_data)



def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def check_expiry_year(value):
    today = datetime.datetime.now()
    if int(value) < today.year:
        raise serializers.ValidationError("Invalid expiry year.")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")


def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")

class PaymentSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_month]
    )
    expiry_year = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_year]
    )
    cvc = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_cvc]
    )