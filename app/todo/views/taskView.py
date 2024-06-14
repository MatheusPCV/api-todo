from ..serializers.taskSerializer import TaskSerializer
from ..repositories.repository import Repository
from ..repositories.taskRepository import TaskRepository
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.urls import reverse
from .loginUserView import LoginUserView
from ..authentication import verifyToken
from django.conf import settings
import jwt


class TaskView(APIView):

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

    def get(self, request):
        if not self.authenticate:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )

        repository = TaskRepository(collection="tasks")

        tasks = repository.filter(username=self.user)
        serializer = TaskSerializer(tasks, many=True)
        serialized_tasks = serializer.data

        for task in serialized_tasks:
            task["id"] = str(task.pop("_id"))

        if self.authenticate:
            return render(request, "home.html", {"tasks": serialized_tasks})
        else:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )

    def post(self, request, id=None):
        if request.POST.get('_method') == 'DELETE':
            return self.delete(request, id)
        if not self.authenticate:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )

        repository = Repository(collection="tasks")
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():

            serializer.validated_data["username"] = self.user
            new_task = repository.insert(serializer.validated_data)

            return redirect("tasks")
        else:
            repository = TaskRepository(collection="tasks")
            tasks = repository.filter(username=self.user)
            serializer = TaskSerializer(tasks, many=True)
            serialized_tasks = serializer.data

            context = {"tasks": serialized_tasks, "error": "Limite de caracteres: 255"}
            return render(request, "home.html", context)


    def delete(self, request, id):
        if not self.authenticate:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )
        
        repository = Repository(collection="tasks")
        repository.delete(id)

        repository = TaskRepository(collection="tasks")

        tasks = repository.filter(username=self.user)
        serializer = TaskSerializer(tasks, many=True)
        serialized_tasks = serializer.data

        for task in serialized_tasks:
            task["id"] = str(task.pop("_id"))

        if self.authenticate:
            return render(request, "home.html", {"tasks": serialized_tasks})
        else:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )
        

