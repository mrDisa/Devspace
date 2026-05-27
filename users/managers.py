from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import F, Count, FloatField, ExpressionWrapper, Sum, Value
from django.db.models.functions import Coalesce

class CustomUserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def with_rank_score(self):
        return self.get_queryset().with_rank_score()

class UserQuerySet(models.QuerySet):
    def with_rank_score(self):
        return self.annotate(
            posts_count=Count("posts", distinct=True),
            posts_comments=Count("posts__comments", distinct=True),

            total_post_likes=Count("posts__likes", distinct=True),
            total_comment_likes=Count("comments__likes", distinct=True),
            total_post_score=Coalesce(
                Sum("posts__score", distinct=True),
                Value(0.0)
            ),
        ).annotate(
            calculated_rank_score=ExpressionWrapper(
                (   
                    F("total_post_score") * 300 +
                    F("posts_count") * 5 +
                    F("posts_comments") * 0.5 +
                    F("total_post_likes") * 2 +
                    F("total_comment_likes") * 0.2
                ),
                output_field=FloatField()
            )
        )