class GameStats:
    """Отслеживает статистику для игры "Инопланетное вторжение"."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings =ai_game.settings # Настройки
        self.reset_stats() # Сброс к начальным значениям

        # Рекорд не должен сбрасываться при новой игре
        self.high_score = 0
        
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ship_left = self.settings.ship_limit # Количество жизней
        self.score = 0 # Текущий счет
        self.level = 1 # Текущий уровень
        

        