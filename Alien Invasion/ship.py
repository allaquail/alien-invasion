import pygame # Импортируем основную библиотеку для создания игр
import os # Импортируем модуль для работы с файловой системой
from pygame.sprite import Sprite # Импортируем базовый класс Sprite для создания игровых объектов

class Ship(Sprite):
    """Класс для управления анимированным кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()  # Вызываем конструктор родительского класса Sprite
        self.screen = ai_game.screen # Сохраняем ссылку на экран игры для отрисовки
        self.settings = ai_game.settings # Сохраняем ссылку на настройки игры
        self.screen_rect = ai_game.screen.get_rect()  # Получаем прямоугольник экрана для позиционирования
        
        # Загрузка кадров анимации
        self.frames = []
        self._load_frames()  # Загружаем все кадры анимации
        
        # Анимация
        self.current_frame = 0 # Индекс текущего отображаемого кадра
        self.animation_counter = 0 # Счетчик для контроля скорости анимации
        self.image = self.frames[self.current_frame] # Устанавливаем текущее изображение корабля (первый кадр)
        self.rect = self.image.get_rect() # Получаем прямоугольник изображения для позиционирования и коллизий
        
        # Позиционирование корабля в центре нижней части экрана
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Сохранение точной координаты X в формате float для плавного движения
        self.x = float(self.rect.x)
        
        # Флаги перемещения - отслеживают нажатые клавиши управления
        self.moving_right = False # Флаг движения вправо (клавиша D)
        self.moving_left = False # Флаг движения влево (клавиша A)

    def _load_frames(self):
        """Загружает все кадры анимации корабля."""
        for i in range(self.settings.ship_frame_count):
            frame_path = os.path.join(self.settings.ship_frames_path, f"ship_frame_{i}.png") # Формируем путь к файлу с кадром анимации
            frame = pygame.image.load(frame_path).convert_alpha()  # Загружаем изображение кадра с сохранением прозрачности
            
            # Масштабируем изображение, если масштаб не равен 1.0
            if self.settings.ship_scale != 1.0:
                original_size = frame.get_size()  # Получаем оригинальные размеры изображения
                # Вычисляем новые размеры с учетом масштаба
                new_size = (int(original_size[0] * self.settings.ship_scale), 
                            int(original_size[1] * self.settings.ship_scale))
                # Масштабируем изображение до новых размеров
                frame = pygame.transform.scale(frame, new_size)
            # Добавляем обработанный кадр в список кадров
            self.frames.append(frame)
            
    def update(self):
        """Обновляет позицию корабля с учетом флагов и анимации."""
        # Обновление позиции вправо, если установлен флаг и корабль не у правого края
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Обновление позиции влево, если установлен флаг и корабль не у левого края
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Обновление целочисленной координаты прямоугольника из точной координаты X
        self.rect.x = self.x
        
        # Обновление анимации корабля
        self._update_animation()

    def _update_animation(self):
        """Обновляет анимацию корабля."""
        self.animation_counter += 1 # Увеличиваем счетчик анимации
        # Проверяем, достиг ли счетчик значения, при котором нужно сменить кадр
        if self.animation_counter >= self.settings.ship_animation_speed:
            self.animation_counter = 0 # Сбрасываем счетчик
            # Переходим к следующему кадру
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            # Устанавливаем новое изображение корабля
            self.image = self.frames[self.current_frame]

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        # Рисуем текущее изображение корабля в его текущей позиции
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней части экрана."""
        # Устанавливаем корабль в центре нижней части экрана
        self.rect.midbottom = self.screen_rect.midbottom
        # Обновляем точную координату X в соответствии с новой позицией
        self.x = float(self.rect.x)