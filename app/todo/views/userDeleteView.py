from ..serializers.userSerializer import UserSerializer
from ..serializers.taskSerializer import TaskSerializer
from ..repositories.repository import Repository
from ..repositories.taskRepository import TaskRepository
from ..repositories.userRepository import UserRepository
from rest_framework.views import APIView, Response, status
from pymongo.errors import DuplicateKeyError
from django.shortcuts import redirect, render
from django.urls import reverse
from ..authentication import verifyToken
from django.conf import settings
import jwt


class UserDeleteView(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.authenticate = False
        self.user = None
        token = request.COOKIES.get("jwt")

        if token:
            try:
                payload = jwt.decode(
                    token, key=getattr(settings, "SECRET_KEY"), algorithms=["HS256"]
                )
                self.user = payload["username"]
                error_code, _ = verifyToken(token)
                if error_code == 0:
                    self.authenticate = True
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass

        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if not self.authenticate:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )

        username = self.user
        repository = UserRepository(collection="users")

        user = repository.get_user_by_username(username)
        user_id = user["_id"]

        repository = Repository(collection="users")
        repository.delete(user_id)

        response = redirect(reverse("home"))
        response.delete_cookie("jwt")
        return response
