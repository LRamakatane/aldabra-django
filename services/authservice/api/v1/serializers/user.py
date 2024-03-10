#!/usr/bin/env python3
"""user serializer module"""
from core.models import User
from rest_framework import serializers
from django.contrib.auth.models import Group
from core.models import Role, Doctor, Patient


class UserSerializer(serializers.ModelSerializer):
    """serializes and deserializes user class"""

    user_groups = serializers.ListField(required=False)
    user_roles = serializers.ListField(required=False)

    class Meta:
        """Meta data defination for user serializer"""

        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "groups": {"read_only": True},
            "user_permissions": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
            "roles": {"read_only": True},
        }

    def create_profile(self, roles, user):

        model_methods = {"patient": Patient.objects.create, "doctor": Doctor.objects.create}

        try:
            for role in roles:
                if isinstance(role, int):
                    role_object = Role.objects.get(pk=role)
                    role = role_object.name

                func = model_methods.get(role.lower(), None)
                if func is not None:
                    func(user=user)
        except Exception as error:
            raise error

    def create(self, validated_data):
        roles = []
        groups = []
        # if groups
        if validated_data.get("user_groups"):
            # get group names and remove from dictionary
            group_names = validated_data.pop("user_groups")

            if group_names:
                # for each name in group_names
                # get group object by name
                # and add group primary_key
                # to group list
                for name__id in group_names:
                    group = (
                        Group.objects.get(name=name__id)
                        if type(name__id) is str
                        else Group.objects.get(pk=name__id)
                    )
                    groups.append(group.pk)
        # if roles
        if validated_data.get("user_roles"):
            # get role names and remove from dictionary
            role_names = validated_data.pop("user_roles")
            if role_names:
                # for each name in role_names
                # get role object by name
                # and add role primary_key
                # to role list
                for name__id in role_names:
                    role = (
                        Role.objects.get(name=name__id)
                        if type(name__id) is str
                        else Role.objects.get(pk=name__id)
                    )
                    roles.append(role.pk)
        try:
            # remove user_groups and user_roles from validated_data
            validated_data.pop("user_roles")
            validated_data.pop("user_groups")
        except KeyError:
            pass

        try:
            # create user object
            # and call .set_password
            # this sets and hash password correctly
            user = User.objects.create(**validated_data)
            user.set_password(validated_data["password"])
            user.save()

            #
            if groups:
                user.groups.set(groups)
                user.save()
            if roles:
                user.roles.set(roles)
                self.create_profile(role_names, user)
        except Exception as error:
            raise Exception(error)
        return user

    def update(self, instance, validated_data):
        roles = []
        groups = []

        if validated_data.get("password"):
            validated_data.pop("password")
            print(
                "cannot update password from here use change password endpoint, password not updated"
            )

        # if groups
        if validated_data.get("user_groups"):
            # get group names and remove from dictionary
            group_names = validated_data.pop("user_groups")

            if group_names:
                # for each name in group_names
                # get group object by name
                # and add group primary_key
                # to group list
                for name__id in group_names:
                    group = (
                        Group.objects.get(name=name__id)
                        if type(name__id) is str
                        else Group.objects.get(pk=name__id)
                    )
                    groups.append(group.pk)
        # if roles
        if validated_data.get("user_roles"):
            # get role names and remove from dictionary
            role_names = validated_data.pop("user_roles")
            if role_names:
                # for each name in role_names
                # get role object by name
                # and add role primary_key
                # to role list
                for name in role_names:
                    role = Role.objects.get(name=name)
                    roles.append(role.pk)
        try:
            validated_data.pop("user_roles")
            validated_data.pop("user_groups")
        except KeyError:
            pass

        try:
            # update user object
            user = instance
            user.__dict__.update(**validated_data)
            user.save()

            # update user groups
            # and user roles
            if groups:
                user.groups.set(groups)
                user.save()
            if roles:
                user.roles.set(roles)
        except Exception as error:
            raise Exception(error)
        return user


class UserCustomerSerializer(serializers.ModelSerializer):
    """create a customer from a user"""

    full_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=True)

    class Meta:
        """class meta data"""

        model = User
        fields = {"email", "password"}

        # makes password write only
        # this way user's can't see password characters
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """create a customer object"""
        # creat's a customer object by calling
        # .create_customer user object manager method
        try:
            user = User.objects.create_customer(**validated_data)
        except Exception as error:
            raise Exception(error)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    """json serializer for changing user password"""

    new_password = serializers.CharField(required=True)
    verify_password = serializers.CharField(required=True)

    class Meta:
        """json meta data"""

        model = User
        fields = ["new_password", "verify_password"]

    @staticmethod
    def verify_new_password(data):
        if data.get("verify_password") == data.get("new_password"):
            return True
        return False


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]
