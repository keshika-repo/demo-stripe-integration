from datetime import datetime, time,timedelta
import json
from rest_framework.views import APIView
from app.models import NewUser,TodoModel
from  app.serializers import UserSerializer,LoginSerializer,TaskSerilaizer,PaymentSerializer
from django.http import JsonResponse
import jwt
from rest_framework.response import Response
from project import settings
from rest_framework.exceptions import AuthenticationFailed
import stripe
from rest_framework import status
from rest_framework.decorators import api_view


class UserView(APIView):
    
    def post(self,request,*args, **kwargs):
        users = UserSerializer(data=request.data)
        users.is_valid(raise_exception=True)
        users.save()
        return JsonResponse({'success':'registered'})
    
    def put(self,request,id):
        user = NewUser.objects.filter(id=id).first()
        if user is not None:
            serializer = UserSerializer(user,data=request.data)
            serializer.is_valid()
            serializer.save()
            res = Response()
            res.data={
                'message':'updated user details',
                'user details':serializer.data
            }
            return res
        return JsonResponse({'msg':'no user found'})
    
class LoginView(APIView):
    def post(self,request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user =  NewUser.objects.filter(email=email,password=password).first()
        serializer = LoginSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if user is not None:
            payload={
              'id':user.id,
              'exp': datetime.utcnow()+ timedelta(minutes=60),
              'iat':datetime.utcnow()
          }
            token = jwt.encode(payload,settings.SECRET_KEY, algorithm='HS256')
            response = Response()
            response.data = {'jwt': token,
                            'msg': 'logged succesfully ' + user.name }
            response.set_cookie(key='jwt', value=token, httponly=True)
            return response
        
class TaskView(APIView):   
    def post(self,request):
        email = request.data.get('email')
        status = request.data.get('status')
        user = NewUser.objects.filter(email = email).first()
        if user is not None :
            task = TaskSerilaizer(data=request.data)
            task.is_valid(raise_exception=True)
            task.save()
            if status == True:
                return JsonResponse({'status':'moved to payment page'})
            return JsonResponse({'status':'status is false'})
        return JsonResponse({'failed':'user not found'})
    
    def put(self,request,id):
        user = TodoModel.objects.filter(id=id).first()
        if user is not None:
            serializer = TaskSerilaizer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = Response()
            res.data = {
                'message':'updated task',
                'details':serializer.data
            }
            return res
        return JsonResponse({'msg':'failed because no user found'})

     
class Userview(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('user authentication failed')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms = 'HS256')
        except jwt.SignatureError:
            raise AuthenticationFailed('invalid')
        user = NewUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class AdminView(APIView):

    def get(self,request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if email == 'admin@gmail.com' and password == 'admin':
            user = NewUser.objects.all()
            task = TodoModel.objects.all()
            serializer = UserSerializer(user,many = True)
            serializer1 = TaskSerilaizer(task,many=True)
            res = Response()
            res.data={
                'User Details':serializer.data,
                'Task Details':serializer1.data
            }
            return res
        return JsonResponse({'msg':'not found'})
    




#     def stripe_card_payment(self, data_dict):
#         try:
#             card_details = {
#                     "number": data_dict['card_number'],
#                     "exp_month": data_dict['expiry_month'],
#                     "exp_year": data_dict['expiry_year'],
#                     "cvc": data_dict['cvc'],
#                 }
            
#             #  you can also get the amount from databse by creating a model
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=10000, 
#                 currency='inr',
#                 payment_method_types=['card'],
#             )
#             payment_intent_modified = stripe.PaymentIntent.modify(
#                 payment_intent['id'],
#             )
#             try:
#                 payment_confirm = stripe.PaymentIntent.confirm(
#                     payment_intent['id']
#                 )
#                 payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
#             except:
#                 payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
#                 payment_confirm = {
#                     "stripe_payment_error": "Failed",
#                     "code": payment_intent_modified['last_payment_error']['code'],
#                     "message": payment_intent_modified['last_payment_error']['message'],
#                     'status': "Failed"
#                 }
#             if payment_intent_modified['status'] == 'succeeded':
#                 response = {
#                     'message': "Card Payment Success",
#                     'status': status.HTTP_200_OK,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent_modified,
#                     "payment_confirm": payment_confirm
#                 }
#             else:
#                 response = {
#                     'message': "Card Payment Failed",
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent_modified,
#                     "payment_confirm": payment_confirm
#                 }
#         except Exception as e:
#               response = {
#                     'message': "Card Payment Failed",
#                     'status': status.HTTP_400_BAD_REQUEST,

#                 }
            
        return response
    
    # def stripe_card_payment(self, data_dict):
    #     try:
    #         card_details = {
    #          "number": data_dict['card_number'],
    #         "exp_month": data_dict['expiry_month'],
    #         "exp_year": data_dict['expiry_year'],
    #         "cvc": data_dict['cvc'],
    #          }

    #     # Step 1: Retrieve the PaymentMethod
    #         payment_method = stripe.PaymentMethod.retrieve(
    #         card_details['prod_OqF36kyuSDqtiP'],  # Replace with the actual PaymentMethod ID
    #     )

    #     # Step 2: Attach the PaymentMethod to the customer
    #         customer = stripe.Customer.create(
    #         payment_method=payment_method.id,
    #         email=data_dict['keshiramesh1804@gmail.com'],  # Replace with the customer's email
    #     )

    #     # Step 3: Update the PaymentIntent with the attached PaymentMethod
    #         payment_intent = stripe.PaymentIntent.create(
    #         amount=10000,
    #         currency='inr',
    #         customer=customer.id,
    #         payment_method=payment_method.id,
    #     )

    #     # Step 4: Confirm the PaymentIntent
    #         payment_intent_modified = stripe.PaymentIntent.confirm(
    #         payment_intent['id']
    #     )

    #         if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
    #             response = {
    #             'message': "Card Payment Success",
    #             'status': status.HTTP_200_OK,
    #             "card_details": card_details,
    #             "payment_intent": payment_intent_modified,
    #          }
    #         else:
    #             response = {
    #             'message': "Card Payment Failed",
    #             'status': status.HTTP_400_BAD_REQUEST,
    #             "card_details": card_details,
    #             "payment_intent": payment_intent_modified,
    #         }
    #     except Exception as e:
    #         response = {
    #         'message': "Card Payment Failed",
    #         'status': status.HTTP_400_BAD_REQUEST,
    #     }

    #     return response
    
    
    
class PaymentAPI(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}
        
        if serializer.is_valid():
            data_dict = serializer.data

            stripe.api_key = settings.STRIPE_SECRET_KEY
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status':
                status.HTTP_400_BAD_REQUEST
                }
                
        return Response(response)

    import stripe

    def stripe_card_payment(self, data_dict):
        try:
        # Step 1: Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=100,
                currency='inr',
                payment_method_types=['card'],
                setup_future_usage='off_session'
            )
            
         
            payment_intent_modified = stripe.PaymentIntent.retrieve
        # Step 2: Retrieve the client secret
            client_secret = payment_intent.client_secret

        # Step 3: Pass the client secret to the client-side

        # Step 4: Handle the payment confirmation on the client-side using Stripe.js

        # Step 5: Retrieve the PaymentIntent on the server-side
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent.id)

            if  payment_intent.status == 'succeeded':
                response = {
                'message': "Card Payment Success",
                'status': status.HTTP_200_OK,
                "payment_intent": payment_intent.id,
            }
            else:
                response = {
                'message': "Card Payment Failed",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": payment_intent.id,
            }
        except Exception as e:
                response = {
                'message': "Card Payment Failed",
                'status': status.HTTP_400_BAD_REQUEST,
                }

        return response






from hashlib import sha256

# import requests
# import stripe

# webhook_url = ''
 # whsec_..
# webhook_json_file = 'PATH_TO_JSON_FILE_WITH_WH_DATA/webhook_example.json'


# def generate_stripe_signature_header(payload: str):
#     timestamp_utc = int(time.time())
#     signed_payload = "%d.%s" % (timestamp_utc, payload)
#     v1_sig = compute_signature(signed_payload, secret=stripe_secret)
#     return f't={timestamp_utc},v1={v1_sig}'


# def compute_signature(payload: str, secret):
#     """Take from stripe"""
#     mac = hmac.new(
#         secret.encode("utf-8"),
#         msg=payload.encode("utf-8"),
#         digestmod=sha256,
#     )
#     return mac.hexdigest()


# with open(webhook_json_file, 'r') as f:
#     payload = f.read()

@api_view(['POST'])
def webhooks(request):
    event = None
    payload = request.body
    headers = request.headers['STRIPE_SIGNATURE']
#     signature = generate_stripe_signature_header(payload=payload)

#     headers = {
#     'STRIPE-SIGNATURE': signature,  
#     'Content-Type': 'application/json',
# }
    stripe_secret = 'whsec_ZrhUvDYnvJf5sqJ5UZXEMMCBiezlNKZa' 
    try:
        event = stripe.Webhook.construct_event(
            payload, headers, stripe_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
      
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'data':True})