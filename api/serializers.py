from rest_framework import serializers

class CodeSubmissionSerializer(serializers.Serializer):
    language = serializers.CharField()
    code = serializers.CharField()
    number_of_testcases = serializers.IntegerField()
    time_limit = serializers.IntegerField()
    inputs = serializers.ListField(child=serializers.CharField())
