from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .transport_solver import solve_transport_problem

class TransportSolverView(APIView):
    def post(self, request):
        try:
            result = solve_transport_problem(request.data)
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
