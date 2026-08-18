## Django
from django.utils.text import slugify

## DRF
from rest_framework import serializers

## Local
from communities.models import Community, CommunityMember
from users.serializers import UserSerializer

class CommunitySerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField(read_only=True)
    post_count = serializers.SerializerMethodField(read_only=True)
    is_joined = serializers.SerializerMethodField(read_only=True)
    current_role = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(
        read_only=True
    )

    class Meta:
        model = Community
        fields = [
            'id','name','slug','description','avatar','banner',
            'category','stack','is_private','is_verified','created_at',
            'updated_at', 'member_count', 'post_count', 'is_joined',
            'current_role', 'owner',
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_post_count(self, obj):
        return obj.posts.count()

    def get_member(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        return obj.members.filter(user=request.user).first()

    def get_is_joined(self, obj):
        return bool(self.get_member(obj))

    def get_current_role(self, obj):
        member = self.get_member(obj)
        return member.role if member else None

    def get_owner(self, obj):
        owner = obj.members.filter(role=CommunityMember.Role.OWNER).select_related("user").first()
        return UserSerializer(owner.user, context=self.context).data if owner else None

    def validate(self, attrs):
        if "name" in attrs:
            slug = slugify(attrs["name"])

            queryset = Community.objects.filter(slug=slug)

            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError({
                    "name": "Сообщество с таким названием уже существует."
                })

            attrs["slug"] = slug

        return attrs


class CommunityMemberSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CommunityMember
        fields = ['community', 'user', 'role', 'joined_at',]

    def get_user(self, obj):
        return {
            "id": obj.user_id,
            "username": obj.user.username,
            "avatar": obj.user.avatar.url if obj.user.avatar else None,
        }
