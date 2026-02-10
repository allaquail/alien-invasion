import os # Для работы с файловой системой
import pygame # Основная библиотека для создания игры

class Background:
    """Класс для анимированного фона."""

    def __init__(self, ai_game):
        """Инициализирует анимированный фон."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.frames = []  # Список кадров
        self.current_frame = 0  # Текущий кадр
        self.animation_counter = 0  # Счетчик анимации

        # Загрузка всех кадров фона
        for i in range(self.settings.bg_frame_count):  # Для каждого кадра
            frame_path = os.path.join(self.settings.bg_frames_path, f"frame_{i}.png")
            frame = pygame.image.load(frame_path)  # Загрузка изображения
            # Масштабирование под размер экрана
            frame = pygame.transform.scale(frame, (self.settings.screen_width, self.settings.screen_height))
            self.frames.append(frame)  # Добавление в список

    def update(self):
        """Обновляет текущий кадр анимации."""
        self.animation_counter += 1
        if self.animation_counter >= self.settings.bg_animation_speed:
            self.animation_counter = 0  # Сброс счетчика
            # Переход к следующему кадру (циклически)
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self):
        """Рисует текущий кадр фона."""
        self.screen.blit(self.frames[self.current_frame], (0, 0))  # Отрисовка в левом верхнем углу