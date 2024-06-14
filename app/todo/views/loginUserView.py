from ..serializers.loginSerializer import LoginSerializer
from ..repositories.userRepository import UserRepository
from rest_framework.views import APIView, Response, status
from django.shortcuts import redirect, render
from ..authentication import generateToken


class LoginUserView(APIView):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            repository = UserRepository(collection="users")
            user = repository.get_user_by_username(username)

            if user and user["password"] == password:
                token = generateToken(user)
                response = redirect("tasks/")
                response.set_cookie("jwt", token)
                return response
            else:
                context = {"error": "Authentication failed"}
                return render(request, "login.html", context)
        else:
            context = {"error": "Invalid data"}
            return render(request, "login.html", context)
