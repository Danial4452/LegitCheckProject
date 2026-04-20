from rest_framework import serializers

# Serializer — для логина (не ModelSerializer)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# Serializer — для регистрации (не ModelSerializer)
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email    = serializers.EmailField(required=False)