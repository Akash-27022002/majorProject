from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_decode_handler
from predicition.serializer import *
import json
from django.utils.translation import gettext as _
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array,load_img
# Create your views here.
img_height, img_width = 224, 224
jsonFilePath = 'model/categories.json'
modelFilePath = "model/plant_disease_detection.h5"
def perdictImage(imagepath):
        with open(jsonFilePath) as jsonData:
            output_dict = json.load(jsonData)
        # print(output_dict)
        output_list = list(output_dict.keys())
        model = load_model(modelFilePath)
        img = load_img(imagepath, target_size=(img_height, img_width))
        x = img_to_array(img)
        x = x/255
        x = x.reshape(1, img_height, img_width, 3)
        predi = model.predict(x)
        result = output_list[np.argmax(predi[0])]
        return result

def verifyToken(token):
    try:
        decode = jwt_decode_handler(token)
        return decode
    except:
        return {"result" : False }

class Predicition(APIView):
    
    def get(self,request):
    #    result = perdictImage("media/projectmedia/image_3.JPG")
        # prediction = Predictions.objects.get(id=2)
        user = User.objects.get(id=6)
        ans = UserSerializer(user,).data
        print(ans)
        # print(prediction)
        # prediction.output = "eagle"
        # prediction.save()
        return Response({"message":"post prediction","res":1},status=status.HTTP_200_OK)
    
    def post(self,request):
        authToken = request.headers['Authorization'].split()[1]
        user = verifyToken(authToken)
        print(user)
        data = request.data
        print("data",data)
        context = {}
        form = PredicitionSerializer(data=data)
        if not form.is_valid():
            return Response(
                {"error": True, "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            form.save()
            formData = form.data
            img_path = formData["image"]
            output = perdictImage(imagepath=img_path[1:])
            prediction = Predictions.objects.get(id=formData["id"])
            users = User.objects.get(id=user['id'])
            users.history.add(prediction)
            prediction.output = output
            prediction.save()
            context['result'] = output
            return Response(context, status=status.HTTP_200_OK)
        
class RegistrationView(APIView):
    def post(self,request):
        data = request.data
        print("akash",data)
        return Response({"msg":"success"},status=status.HTTP_200_OK)
        form = RegisterSerializer(data=data)
        if form.is_valid():
            name = data['name']
            email = data['email']
            password = data['password']
            user = User(email = email,name=name,)
            # user.history.set(None)
            user.set_password(password)
            user.save()
            return Response(
                    {"error": False, "message": "User created Successfully."},
                    status=status.HTTP_200_OK,
                )
        return Response({'error': True, 'errors': form.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    

def jwt_payload_handler(user):
    return {
        "id" :user.pk,
        "email":user.email,
        "name":user.name,
    }

class LoginView(APIView):
        def post(self,request):
            data =  request.data
            email = data["email"]
            password = data["password"]
            errors = {}
            if not email:
                errors['email'] = ['This field is required']
            if not password:
                errors['password'] = ['This field is required']
            if errors:
                return Response({'error': True, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": True, "errors": "user not avaliable in our records"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password):
                payload = jwt_payload_handler(user)
                response_data = {
                    "token": jwt_encode_handler(payload),
                    "error": False,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            password_field = "doesnot match"
            msg = _("Email and password {password_field}")
            msg = msg.format(password_field=password_field)
            return Response(
                {"error": True, "errors": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

class DecodeToke(APIView):
    def post(self,request):
        # token = request.headers['Authorization'].split()[1]
        data = request.data
        token = data['token']
        x = jwt_decode_handler(token)
        print(x['id'])
        # print(x["id"])
        return Response({"mes":"success"},status=status.HTTP_200_OK)
    

"""
{
"name":"akash",
"email":"akash12@gmail.com",
"password":"pass2023"
}


"""