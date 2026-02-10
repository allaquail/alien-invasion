import pygame # Основная библиотека для создания игры
import os # Для работы с файловой системой
from pygame.sprite import Sprite # Базовый класс для игровых объектов в PyGame

class AnimatedBullet(Sprite):
    """Класс для управления анимированными снарядами."""
    
    def __init__(self, ai_game):
        # Вызываем конструктор родительского класса Sprite
        super().__init__()  # Инициализация Sprite
        self.screen = ai_game.screen # Сохраняем ссылку на экран из главной игры
        self.settings = ai_game.settings # Сохраняем ссылку на настройки игры
        self.ai_game = ai_game # Ссылка на самую главную игру
        
        # Загрузка кадров анимации
        self.frames = []
        self._load_frames()
        
        # Установка начального кадра
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()  # Прямоугольник для коллизий
        
        # Позиционирование пули в центре верхней части корабля
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Позиция в вещественном формате для плавного движения
        self.y = float(self.rect.y)
    
    def _load_frames(self):
        """Загружает все кадры анимации."""
        for i in range(self.settings.bullet_frame_count):
            frame_path = os.path.join(self.settings.bullet_frames_path, f"bullet_frame_{i}.png")
            frame = pygame.image.load(frame_path).convert_alpha()  # С альфа-каналом (загрузка прозрачных картинок в PyGame)
            
            # Масштабирование если нужно
            if self.settings.bullet_scale != 1.0:
                original_size = frame.get_size()
                new_size = (int(original_size[0] * self.settings.bullet_scale), 
                            int(original_size[1] * self.settings.bullet_scale))
                frame = pygame.transform.scale(frame, new_size)
            self.frames.append(frame)  # Добавление кадра
                
    def update(self):
        """Обновляет позицию и анимацию пули."""
        # Движение вверх
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y  # Обновление прямоугольника
        
        # Анимация
        self.animation_counter += 1
        if self.animation_counter >= self.settings.bullet_animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def draw_bullet(self):
        """Выводит пулю на экран."""
        self.screen.blit(self.image, self.rect)