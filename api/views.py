import subprocess
import tempfile
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSubmissionSerializer

@api_view(['POST'])
def test_submission(request):
    serializer = CodeSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        language = serializer.validated_data['language']
        code = serializer.validated_data['code']
        number_of_testcases = serializer.validated_data['number_of_testcases']
        time_limit = serializer.validated_data['time_limit']
        inputs = serializer.validated_data['inputs']


        # NEED TO FIX DOCKER MOUNT FILES PERMISSIONS
        # with tempfile.NamedTemporaryFile(delete=False, mode='w') as input_file:
        #     input_file.write(str(inputs))
        # input_file_path = os.path.join(tempfile.gettempdir(), input_file.name)
        # os.chmod(input_file_path, 0o644)
        # "-v", f"{input_file_path}:/app/input.txt",

        command = [
            "docker", "run",
            "--rm",
            "-e", f"INPUTS={inputs}",
            "-e", f"LANGUAGE={language}",
            "-e", f"CODE={code}",
            "-e", f"NUMBER_OF_TESTCASES={number_of_testcases}",
            "-e", f"TIME_LIMIT={time_limit}",
            "docker-safe-env"
        ]
        try:
            output = subprocess.check_output(command, text=True).splitlines()
            return Response({'results': output}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
