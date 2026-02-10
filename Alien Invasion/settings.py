import os # Импортируем модуль для работы с файловой системой

# Класс для хранения всех настроек игры
class Settings:
    def __init__(self):
        self.screen_width = 1200 # Ширина экрана в пикселях
        self.screen_height = 900 # Высота экрана в пикселях
        self.bg_color = (0, 33, 55) # Цвет фона
        
        # Настройки анимированного фона
        self.bg_frames_path = os.path.join("images", "bg_frames")  # Путь к кадрам фона
        self.bg_frame_count = 44 # Количество кадров в анимации фона
        self.bg_animation_speed = 2 # Скорость анимации фона (чем меньше, тем быстрее)

        # Настройки корабля
        self.ship_speed = 11.0 # Скорость движения корабля (в пикселях за кадр)
        self.ship_limit = 3 # Максимальное количество жизней

        # Параметры снаряда
        self.bullet_speed = 5.0 # Скорость пули
        self.bullet_width = 5.5 # Ширина пули в пикселях
        self.bullet_height = 15 # Высота пули в пикселях
        self.bullet_color = (183, 132, 167) # Цвет пули
        self.bullets_allowed = 4 # Максимальное количество пуль на экране одновременно

        # Параметры анимированного снаряда
        self.bullet_frames_path = os.path.join("images", "bullet_frames") # Путь к кадрам пули
        self.bullet_frame_count = 4  # Количество кадров в анимации пули
        self.bullet_animation_speed = 3 # Скорость анимации пули
        self.bullet_scale = 0.05 # Масштаб изображения пули

        # Настройки звука и музыки
        self.music_volume = 0.5 # Громкость фоновой музыки (от 0.0 до 1.0)
        self.music_path = os.path.join("sounds", "background_music.mp3") # Путь к файлу музыки
        self.sound_effects_volume = 0.7 # Громкость звуковых эффектов

        # Настройки анимированного корабля
        self.ship_frames_path = os.path.join("images", "ship_frames") # Путь к кадрам корабля
        self.ship_frame_count = 8  # Количество кадров в анимации корабля
        self.ship_animation_speed = 5 # Скорость анимации корабля
        self.ship_scale = 0.6  # Масштаб изображения корабля

        # Настройки анимированных пришельцев
        self.alien_frames_path = os.path.join("images", "alien_frames") # Путь к кадрам пришельца
        self.alien_frame_count = 14 # Количество кадров в анимации пришельца
        self.alien_animation_speed = 6 # Скорость анимации пришельца
        self.alien_scale = 0.27 # Масштаб изображения пришельца
        self.alien_speed = 1.5 # Базовая скорость пришельцев
        self.fleet_drop_speed = 10 # На сколько опускается флот при развороте
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1

        self.alien_speed = 1.5 # Скорость движения пришельцев 
        
        self.fleet_drop_speed = 100 # Скорость опускания флота  

        self.speedup_scale = 1.1 # Темп ускорения игры

        self.score_scale = 1.5 # Множитель для увеличения очков за пришельцев

        self.initialize_dynamic_settings() # Инициализируем динамические настройки

        # Настройки стартового экрана
        self.start_screen_button_x = 955  # X-координата центра кнопки "Play"
        self.start_screen_button_y = 550  # Y-координата центра кнопки "Play"
        self.start_screen_text_x = 970  # X-координата текста подсказки
        self.start_screen_text_y = 1060  # Y-координата текста подсказки
        self.start_screen_text_blink_interval = 30  # Интервал мигания текста в кадрах
        self.start_screen_inactivity_time = 3  # Время бездействия для показа подсказки (в секундах)
        
        # Настройки анимированного фона стартового экрана
        self.start_screen_frames_path = os.path.join("images", "start_screen_frames") # Путь к кадрам
        self.start_screen_frame_count = 39  # Количество кадров в анимации стартового экрана
        self.start_screen_animation_speed = 3.5   # Скорость анимации стартового экрана


    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.bullet_speed = 2.5 # Начальная скорость пули
        self.alien_speed = 0.5 # Начальная скорость пришельцев

        # Начальное направление движения флота
        self.fleet_direction = 1  # 1 = движение вправо, -1 = движение влево

        # Начальное количество очков за одного пришельца
        self.alien_points = 50 # Очки за уничтожение одного пришельца

    # Метод для увеличения сложности игры
    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        # Увеличиваем скорости всех объектов
        self.ship_speed *= self.speedup_scale # Увеличиваем скорость корабля
        self.bullet_speed *= self.speedup_scale # Увеличиваем скорость пуль
        self.alien_speed *= self.speedup_scale # Увеличиваем скорость пришельцев


        # Увеличиваем очки за пришельца
        self.alien_points = int(self.alien_points * self.score_scale) # Умножаем и преобразуем в целое число