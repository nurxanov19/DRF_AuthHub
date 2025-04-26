from rest_framework import serializers
from api_auth.models import CustomUser

class AuthOneSerializers(serializers.Serializer):

    phone = serializers.CharField(max_length=200)

    def validate_phone(self, phone):
        if len(str(phone)) != 12 or not phone.isdigit() \
                or str(phone)[:3] != '998':
            raise serializers.ValidationError('Phone is invalid (serializer)')
        return phone


class AuthTwoSerializer(serializers.Serializer):

    key = serializers.CharField(max_length=300)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        key = attrs.get('key')
        code = attrs.get('code')

        if not key or not code:
            raise serializers.ValidationError('Key or code missing (serializer)')

        if len(code) != 6 or not code.isdigit():
            raise serializers.ValidationError("Code must be a 6-digit number.")

        return attrs
