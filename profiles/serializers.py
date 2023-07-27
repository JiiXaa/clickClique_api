from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # is_owner is a custom field that returns True if the user is the owner of the profile. That will help on the frontend to show the edit and delete buttons only to the owner of the profile
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # To get the user, we use self.context["request"].user instead of self.context["request"].data["owner"]
        # The request context is passed to the serializer by the view
        request = self.context["request"]
        return obj.owner == request.user

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "name",
            "content",
            "image",
            "is_owner",
        ]
