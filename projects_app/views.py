from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import (
    get_project_by_id,
    get_full_projects,
    change_employee
)
from .serializers import (
    ProjectSerializer,
    EmployeeProjectsSerializer
)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_project_by_id(project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_full_projects()
        print(data)
        return Response(data)


class ChangeProjectEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        serializer = EmployeeProjectsSerializer(data=request.data, many=True)

        if serializer.is_valid():
            print(serializer.validated_data)
            change_employee(serializer.validated_data)
            return Response(status=200)

        return Response(serializer.errors, status=400)
