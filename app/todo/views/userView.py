from ..serializers.userSerializer import UserSerializer
from ..serializers.taskSerializer import TaskSerializer
from ..repositories.repository import Repository
from ..repositories.taskRepository import TaskRepository
from ..repositories.userRepository import UserRepository
from rest_framework.views import APIView, Response, status
from pymongo.errors import DuplicateKeyError
from django.shortcuts import redirect, render
from django.urls import reverse


class UserView(APIView):

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        if request.POST.get('_method') == 'DELETE':
            username = self.user
            return self.delete(request, username)
        
        repository = UserRepository(collection="users")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                repository.insert(serializer.validated_data)
                return redirect(reverse("home"))

            except DuplicateKeyError as e:
                error_field = "username" if "username" in str(e) else "email"
                context = {"error": f"{error_field} já está em uso"}
                return render(request, "register.html", context)
        else:
            error_message = next(iter(serializer.errors.values()))[0]
            context = {"error": error_message}
            return render(request, "register.html", context)
        
    def delete(self, request, username):
        if not self.authenticate:
            return render(
                request,
                "login.html",
                {"error": "Você precisa estar autenticado para acessar esta página."},
            )
        
        repository = UserRepository(collection="users")
        username = repository.get_user_by_username()
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
        
        
