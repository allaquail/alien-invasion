import os  # Импортируем модуль для работы с файловой системой
import pygame # Основная библиотека для создания игры

class StartScreenBackground:
    """Класс для управления анимированным фоном стартового экрана."""
    
    def __init__(self, ai_game):
        """Инициализирует фон стартового экрана."""
        self.screen = ai_game.screen # Сохраняем ссылку на экран игры для отрисовки
        self.settings = ai_game.settings  # Сохраняем ссылку на настройки игры
        
        # Загрузка кадров анимации
        self.frames = []
        self._load_frames()  # Загружаем все кадры анимации из файлов
        
        self.current_frame = 0  # Устанавливаем начальный кадр анимации
        self.animation_counter = 0  # Создаем счетчик для контроля скорости анимации
        
        # Проверяем, были ли успешно загружены кадры анимации
        if self.frames:
            # Устанавливаем текущее изображение как первый кадр
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect() # Получаем прямоугольник изображения для позиционирования
            self.rect.topleft = (0, 0) # Размещаем изображение в левом верхнем углу экрана
            print(f"Загружено {len(self.frames)} кадров для стартового экрана") # Выводим сообщение о успешной загрузке кадров
        else:
            print("Не удалось загрузить кадры для стартового экрана") # Выводим сообщение об ошибке, если кадры не загружены
    
    def _load_frames(self):
        """Загружает все кадры анимации для стартового экрана."""
        # Проходим по всем кадрам, указанным в настройках
        for i in range(self.settings.start_screen_frame_count):
            frame_path = os.path.join("images", "start_screen_frames", f"frame_{i}.png") # Формируем путь к файлу с текущим кадром анимации
            print(f"Попытка загрузить: {frame_path}") # Выводим путь к файлу
                
            if os.path.exists(frame_path):  # Проверяем, существует ли файл по указанному пути
                frame = pygame.image.load(frame_path).convert_alpha()   # Загружаем изображение кадра с сохранением прозрачности
                    
                # Масштабирование под размер экрана
                if frame.get_size() != self.screen.get_size():
                    # Масштабируем до размеров экрана, указанных в настройках
                    frame = pygame.transform.scale(frame, (self.settings.screen_width, self.settings.screen_height))
                    
                self.frames.append(frame) # Добавляем обработанный кадр в список кадров               
          
    def update(self):
        """Обновляет анимацию фона."""
        if not self.frames:  # Если кадры не загружены, выходим из метода
            return
            
        self.animation_counter += 1 # Увеличиваем счетчик анимации
        # Проверяем, достиг ли счетчик значения для смены кадра
        if self.animation_counter >= self.settings.start_screen_animation_speed:
            self.animation_counter = 0 # Сбрасываем счетчик анимации
            self.current_frame = (self.current_frame + 1) % len(self.frames) # Переходим к следующему кадру
            self.image = self.frames[self.current_frame] # Устанавливаем новое текущее изображение
    
    def draw(self):
        """Рисует текущий кадр анимации."""
        self.screen.blit(self.image, self.rect) # Рисуем текущий кадр анимации в левом верхнем углу экрана
        
        
       