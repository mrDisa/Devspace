from rest_framework import serializers
from .utils import calculate_rank
from users.models import User
from interactions.models import Follow  # Импортируем модель подписок

class UserSerializer(serializers.ModelSerializer):
    # Ранги
    current_rank = serializers.SerializerMethodField()
    next_rank = serializers.SerializerMethodField()
    points_to_next = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    # Подписки
    is_followed = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    # Считаем лайки, комментарии, посты, оценки для ранга
    posts_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    total_post_likes = serializers.FloatField(read_only=True)
    total_comment_likes = serializers.FloatField(read_only=True)
    total_post_score = serializers.FloatField(read_only=True)

    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'email', 'password', 
            'job', 'bio', 'avatar','rank_score', 'current_rank', 'next_rank', 'points_to_next', 'progress', 'is_followed', 'followers_count', 
            'posts_count', 'comments_count', 'total_post_likes', 'total_comment_likes', 
            'total_post_score',

        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'job': {'required': False},
            'bio': {'required': False},
        }

    # Показываем поля в API
    # ПОДПИСКИ 
    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем наличие записи в таблице Follow
            return Follow.objects.filter(follower=request.user, following=obj).exists()
        return False

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()
    
    # РАНГИ
    def get_current_rank(self, obj):
        current_rank, _, _, _ = calculate_rank(obj.rank_score)
        return current_rank

    def get_next_rank(self, obj):
        _, next_rank, _, _ = calculate_rank(obj.rank_score)
        return next_rank

    def get_points_to_next(self, obj):
        _, _, points_to_next, _ = calculate_rank(obj.rank_score)
        return points_to_next
    
    def get_progress(self, obj):
        _, _, _, progress = calculate_rank(obj.rank_score)
        return progress

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name = validated_data.get('first_name', '')
        user.job = validated_data.get('job', '')
        user.bio = validated_data.get('bio', '')
        if 'avatar' in validated_data:
            user.avatar = validated_data['avatar']
            
        user.save()
        return user
    