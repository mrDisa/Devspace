## Django
from django.utils.text import slugify

## DRF
from rest_framework import serializers

## Local
from communities.models import Community, CommunityMember
from users.serializers import UserSerializer

class CommunitySerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Community
        fields = [
            'id','name','slug','description','avatar','banner',
            'category','stack','is_private','is_verified','created_at',
            'updated_at', 'member_count',
        ]

    def validate(self, attrs):
        slug = slugify(attrs["name"])

        if Community.objects.filter(slug=slug).exists():
            raise serializers.ValidationError({
                "name": "Сообщество с таким названием уже существует."
            })

        attrs["slug"] = slug
        return attrs


class CommunityMemberSerializer(serializers.ModelSerializer):
    my_role = serializers.SerializerMethodField()

    class Meta:
        model = CommunityMember
        fields = ['community', 'user', 'role', 'joined_at', 'my_role']