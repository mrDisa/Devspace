from users.models import User
from users.utils import calculate_rank

def update_user_rank(user):
    user_annotated = User.objects.with_rank_score().get(id=user.id)
    score = user_annotated.calculated_rank_score

    current_rank, next_rank, points_to_next, progress = calculate_rank(score)

    user.rank_score = score

    user.save(update_fields=["rank_score",])