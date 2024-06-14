from rest_framework.views import APIView
from django.shortcuts import redirect
from django.urls import reverse

class LogoutUserView(APIView):

    def get(self, request):
        response = redirect(reverse("home"))
        response.delete_cookie("jwt")
        return response