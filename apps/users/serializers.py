from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.email import send_email
from apps.common.serializers import CompanyBaseSerializer, FreelancerBaseSerializer
from apps.common.utils import OTPUtils

from .models import Address, Category, Skill

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """
    serializer for signing up a new user
    """

    password = serializers.CharField(min_length=6, write_only=True)
    password2 = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "password2"]

    # Check if passwords match
    def validate_password2(self, password2: str):
        if self.initial_data.get("password") != password2:
            raise serializers.ValidationError("passwords do not match")
        return password2

    def create(self, validated_data: dict):
        # Remove second password field
        _ = validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class SignupResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "token")

    @swagger_serializer_method(
        serializer_or_field=serializers.JSONField(),
    )
    def get_token(self, user: User):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class ForgotPasswordSerializer(serializers.Serializer):
    """
    serializer for initiating forgot password. Send reset code
    """

    email = serializers.EmailField(required=True)

    def create(self, validated_data: dict):
        """
        if email code to a user, send an email with a code to reset password
        """
        token = ""
        email = validated_data.get("email")
        if user := User.objects.filter(email=email).first():
            code, token = OTPUtils.generate_otp(user)

            # dynamic_data = {"first_name": user.first_name, "verification_code": code}
            send_email(email, "Password Reset", code)

        return {"token": token}


class ResetPasswordSerializer(serializers.Serializer):
    """ """

    token = serializers.CharField(required=True)
    code = serializers.CharField(min_length=6, required=True)
    password = serializers.CharField(min_length=6, required=True)

    def create(self, validated_data):
        """
        reset user password using email as an identification
        """

        token = validated_data.get("token")
        code = validated_data.get("code")
        password = validated_data.get("password")

        data = OTPUtils.decode_token(token)

        if not data or not isinstance(data, dict):
            raise serializers.ValidationError("Invalid token")

        if not (user := User.objects.filter(id=data.get("user_id")).first()):
            raise serializers.ValidationError("User does not exist")

        # validate code
        if not OTPUtils.verify_otp(code, data["secret"]):
            raise serializers.ValidationError("Invalid code")

        # reset password
        user.set_password(raw_password=password)
        user.save()

        return {
            "email": user.email,
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)

    class Meta:
        fields = ("old_password", "new_password")

    def create(self, validated_data):
        request = self.context.get("request")
        user: User = request.user

        if not user.check_password(validated_data.get("old_password")):
            raise serializers.ValidationError({"detail": "Incorrect password"})

        # reset password
        user.set_password(raw_password=validated_data.get("new_password"))
        user.save()

        return {"old_password": "", "new_password": ""}


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


# class ProfileSerializer(serializers.ModelSerializer):
#     email = serializers.SerializerMethodField()
#     address_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Profile
#         fields = (
#             "id",
#             "user",
#             "first_name",
#             "last_name",
#             "email",
#             "address_name",
#             "gender",
#             "dob",
#             "phone_number",
#             "profile_image",
#         )

#     def get_email(self, profile) -> str:
#         return profile.user.email if profile.user else ""

#     def get_address_name(self, profile) -> str:
#         return profile.address.address_name if profile.address else ""


class UserSerializer(serializers.ModelSerializer):
    freelancer = FreelancerBaseSerializer(read_only=True)
    company = serializers.SerializerMethodField()
    # company = CompanyBaseSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "account_type",
            "role",
            "freelancer",
            "company",
        ]
        read_only_fields = ["role", "account_type"]

    @swagger_serializer_method(
        serializer_or_field=CompanyBaseSerializer(),
    )
    def get_company(self, obj):
        company = obj.company.first()
        if company:
            return CompanyBaseSerializer(company).data
        else:
            return None


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
