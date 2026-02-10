import pygame # Основная библиотека для создания игры
import os  # Для работы с файловой системой
from pygame.sprite import Sprite  # Базовый класс для игровых объектов в PyGame

class Alien(Sprite):
    """Класс, представляющий одного анимированного пришельца."""

    def __init__(self, ai_game, x, y):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()  # Инициализация родительского класса Sprite
        self.screen = ai_game.screen  # Экран для отрисовки
        self.settings = ai_game.settings  # Настройки
        self.ai_game = ai_game  # Ссылка на главный объект игры

        # Загрузка кадров анимации пришельца
        self.frames = []  # Список для хранения кадров
        self._load_frames()  # Загрузка кадров из файлов
        
        # Настройки анимации
        self.current_frame = 0  # Текущий кадр
        self.animation_counter = 0  # Счетчик для контроля скорости анимации
        self.image = self.frames[self.current_frame]  # Текущее изображение
        self.rect = self.image.get_rect()  # Прямоугольник для коллизий и позиции

        # Установка позиции пришельца
        self.rect.x = x
        self.rect.y = y

        # Сохранение точной позиции (float для плавного движения)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Направление движения (1 - вправо, -1 - влево)
        self.direction = 1
        
    def _load_frames(self):
        """Загружает все кадры анимации пришельца."""
        for i in range(self.settings.alien_frame_count):  # Для каждого кадра
            # Формирование пути к файлу
            frame_path = os.path.join(self.settings.alien_frames_path, f"alien_frame_{i}.png")
            
            frame = pygame.image.load(frame_path).convert_alpha()  # Загрузка с альфа-каналом (загрузка прозрачных картинок в PyGame)
            
            # Масштабирование если нужно
            if self.settings.alien_scale != 1.0:
                original_size = frame.get_size()
                new_size = (int(original_size[0] * self.settings.alien_scale), 
                        int(original_size[1] * self.settings.alien_scale))
                frame = pygame.transform.scale(frame, new_size)
            self.frames.append(frame)  # Добавление в список кадров
           
    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()  # Получаем размеры экрана
        # Проверяем правый или левый край
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Перемещает пришельцев влево или вправо."""
        # Движение с учетом направления флота
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x  # Обновление прямоугольника
        
        # Анимация
        self._update_animation()
    
    def _update_animation(self):
        """Обновляет анимацию пришельца."""
        self.animation_counter += 1
        if self.animation_counter >= self.settings.alien_animation_speed:
            self.animation_counter = 0  # Сброс счетчика
            # Переход к следующему кадру (циклически)
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]  # Обновление изображения

    def change_direction(self):
        """Изменяет направление движения пришельца."""
        self.direction *= -1  # Меняем направление
        self.y += self.settings.fleet_drop_speed  # Опускаемся
        self.rect.y = int(self.y)  # Обновляем позицию

    def blitme(self):
        """Рисует пришельца."""
        self.screen.blit(self.image, self.rect)  # Отрисовка на экране