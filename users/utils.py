
RANKS = [
    (0, "Наблюдатель"),
    (100, "Активный пользователь"),
    (300, "Полезный пользователь"),
    (800, "Ценный автор"),
    (1500, "Активный автор"),
    (2500, "Влиятельный автор "),
    (4000, "Архитектор"),
    (6000, "Ключевой автор"),
]

def calculate_rank(rank_score):
    if rank_score > RANKS[len(RANKS) - 1][0]:
            
            current_rank = RANKS[len(RANKS) - 1][1]
            next_rank = None
            points_to_next = 0
            progress = f"Максимальный ранг достигнут"

            return current_rank, next_rank, points_to_next, progress 
    for i, (points, rank) in enumerate(RANKS):
        if rank_score < points:

            next_rank = rank

            points_to_next = RANKS[i][0] - rank_score

            current_rank = RANKS[i - 1][1]
            progress = f"{round((rank_score / points_to_next) * 10, 1)} %"

            return current_rank, next_rank, points_to_next, progress

print(calculate_rank(378))