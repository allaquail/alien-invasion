import pygame.font # Импортируем модуль для работы со шрифтами PyGame
import os # Импортируем модуль для работы с файловой системой

class AnimatedLife:
    """Класс для анимированного изображения жизни."""
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen 
        self.frames = [] # Список для хранения кадров анимации жизни
        self.current_frame = 0  # Текущий отображаемый кадр (начинаем с первого)
        self.animation_speed = 8 # Скорость анимации
        self.counter = 0  # Счетчик для отслеживания времени смены кадров
        
        self._load_animation_frames() # Загружаем кадры анимации при создании объекта
        
    def _load_animation_frames(self):
        """Загружает кадры анимации для жизни."""
        self.life_width = 45 # Ширина изображения жизни
        self.life_height = 35 # Высота изображения жизни
        
        for i in range(4):  # Загружаем 4 кадра анимации (от 0 до 3)
            frame_path = f'images/life_frames/life_frame_{i}.png'  # Формируем путь к файлу с кадром
            frame = pygame.image.load(frame_path).convert_alpha()  # Загружаем изображение с сохранением прозрачности
            scaled_frame = pygame.transform.scale(frame, (self.life_width, self.life_height))  # Масштабируем изображение до нужного размера
            self.frames.append(scaled_frame)  # Добавляем масштабированный кадр в список
            print(f"Загружен кадр: {frame_path}") # Выводим сообщение в консоль
               
    def update(self):
        """Обновляет анимацию."""
        self.counter += 1 # Увеличиваем счетчик на 1
        if self.counter >= self.animation_speed:  # Проверяем, пора ли сменить кадр
            self.counter = 0 # Сбрасываем счетчик
            self.current_frame = (self.current_frame + 1) % len(self.frames) # Переходим к следующему кадру 
    
    def get_current_frame(self):
        """Возвращает текущий кадр анимации."""
        return self.frames[self.current_frame] if self.frames else None # Возвращаем текущий кадр, если список кадров не пустой

class Scoreboard:
    """Класс для вывода игровой информации с анимированными жизнями."""

    def __init__(self, ai_game):
        self.ai_game = ai_game # Сохраняем ссылку на главную игру
        self.screen = ai_game.screen  # Сохраняем ссылку на экран
        self.screen_rect = self.screen.get_rect()  # Получаем прямоугольник экрана для позиционирования
        self.settings = ai_game.settings   # Сохраняем ссылку на настройки игры
        self.stats = ai_game.stats  # Сохраняем ссылку на игровую статистику

        self.text_color = (255, 255, 255) # Белый цвет
        self.font = pygame.font.SysFont(None, 48) # Шрифт

        # Создание анимированных жизней
        self.animated_life = AnimatedLife(ai_game)
        
        self.prep_score()  # Подготовка счета
        self.prep_high_score()  # Подготовка рекорда
        self.prep_level()  # Подготовка уровня
        self.prep_ships()  # Подготовка отображения жизней

    def prep_ships(self):
        """Подготавливает позиции для отображения жизней."""
        self.life_positions = [] # Список позиций для жизней
        
        start_x = 40 # Начальная позиция X (от левого края)
        start_y = 35 # Начальная позиция Y (от верхнего края)  
        spacing = 10 # Расстояние между сердечками
        
        life_width = self.animated_life.life_width # Ширина одного сердца
        
        for life_number in range(self.stats.ship_left):
            life_x = start_x + life_number * (life_width + spacing)  # Вычисляем X координату для текущего сердечка
            life_y = start_y # Y координата одинакова для всех сердечек
            self.life_positions.append((life_x, life_y))  # Добавляем координаты в список

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = f"Level {self.stats.level}"   # Создаем строку с номером уровня 
        self.level_image = self.font.render(level_str, True, self.text_color) # Создаем изображение текста
        self.level_image = self.level_image.convert_alpha()  # Изображение с прозрачностью
        
        self.level_rect = self.level_image.get_rect()   # Прямоугольник изображения уровня 
        self.level_rect.right = self.score_rect.right  # Выравниваем правый край уровня с правым краем счета
        self.level_rect.top = self.score_rect.bottom + 10  # Размещаем уровень под счетом с отступом 10 пикселей

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score_str = f"High core: {self.stats.high_score:}"    # Создаем строку с рекордом
        # Создаем изображение текста рекорда
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_image = self.high_score_image.convert_alpha() # Оптимизируем изображение
        
        self.high_score_rect = self.high_score_image.get_rect()   # Получаем прямоугольник изображения рекорда
        self.high_score_rect.centerx = self.screen_rect.centerx # Размещаем рекорд по горизонтальному центру экрана
        self.high_score_rect.top = self.score_rect.top  # Размещаем рекорд на той же высоте, что и счет

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = f"Score: {self.stats.score:}"   # Создаем строку с текущим счетом
        self.score_image = self.font.render(score_str, True, self.text_color)   # Создаем изображение текста счета
        self.score_image = self.score_image.convert_alpha()  # Оптимизируем изображение
        
        self.score_rect = self.score_image.get_rect()    # Получаем прямоугольник изображения счета
        self.score_rect.right = self.screen_rect.right - 20   # Размещаем счет в правом верхнем углу с отступом 20 пикселей
        self.score_rect.top = 20 # Отступ сверху

    def update_animation(self):
        """Обновляет анимацию жизней."""
        self.animated_life.update()

    def show_score(self):
        """Выводит счета, уровень и анимированные жизни на экран."""
        # Отрисовка текстовой информации (счет, рекорд, уровень)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        
        # Отрисовка анимированных жизней
        current_frame = self.animated_life.get_current_frame()
        if current_frame:
            # Для каждой позиции жизни рисуем текущий кадр анимации
            for life_x, life_y in self.life_positions:
                self.screen.blit(current_frame, (life_x, life_y))

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:  # Если текущий счет больше рекорда
            self.stats.high_score = self.stats.score  # Обновляем значение рекорда
            self.prep_high_score()  # Обновление отображения рекорда
            