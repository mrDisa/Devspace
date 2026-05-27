# Список рангов
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
    # Если достигли максимального ранга
    if rank_score > RANKS[len(RANKS) - 1][0]:
            
            current_rank = RANKS[len(RANKS) - 1][1]
            next_rank = None
            points_to_next = 0
            progress = 100

            return current_rank, next_rank, points_to_next, progress 
    for i, (points, rank) in enumerate(RANKS):
        if rank_score < points:

            next_rank = rank

            points_to_next = RANKS[i][0] - rank_score

            current_rank = RANKS[i - 1][1]

            # Порог текущего ранга и следующего
            current_rank_points = RANKS[i - 1][0]
            next_rank_points = RANKS[i][0]

             # Считаем прогресс до следующего ранга(в процентах)
            if next_rank_points == current_rank_points:
                progress = 100
            else:
                progress = round((rank_score - current_rank_points) / (next_rank_points - current_rank_points) * 100)

            return current_rank, next_rank, points_to_next, progress
