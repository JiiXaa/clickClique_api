from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    The create method handles the unique constraint on 'owner' and 'followed'
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    followed = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = [
            "id",
            "created_at",
            "owner",
            "followed",
        ]

    def create(self, validated_data):
        """
        Integrity error is raised if the user tries to follow the same user twice.
        """

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "You are already following this user."}
            )
