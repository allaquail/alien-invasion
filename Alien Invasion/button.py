import pygame.font # Импортируем модуль для работы со шрифтами в PyGame

class Button:
    def __init__(self, ai_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai_game.screen # Получаем доступ к экрану игры для рисования
        self.screen_rect = self.screen.get_rect()  # Получаем прямоугольник экрана для позиционирования
        self.settings = ai_game.settings  # Получаем доступ к настройкам игры
        
        # Устанавливаем размеры кнопки (ширина и высота в пикселях)
        self.width, self.height = 700, 700  # Размер кнопки

        # Устанавливаем цвет фона кнопки 
        self.button_color = (0, 135, 0, 0)  # Прозрачный фон
        self.text_color = (176, 196, 222)  # Светло-синий текст
        self.font = pygame.font.SysFont('harrington', 90, bold=True)  # Шрифт

        msg = msg.upper()  # Преобразуем текст сообщения в верхний регистр (делаем заглавными буквами)

        # Создаем прямоугольник (Rect) для кнопки с указанными размерами
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.settings.start_screen_button_x, 
                           self.settings.start_screen_button_y)
        
        self._prep_msg(msg)  # Вызываем метод для подготовки текстового изображения
        
    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        # Создание изображения текста
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect() # Прямоугольник текстового изображения для позиционирования
        self.msg_image_rect.center = self.rect.center  # Центрирование
        
    def draw_button(self):
        """Отображение пустой кнопки и вывод сообщения."""
        # Обновляем позицию кнопки на случай, если настройки изменились
        self.rect.center = (self.settings.start_screen_button_x, 
                           self.settings.start_screen_button_y)
        self.msg_image_rect.center = self.rect.center # Синхронизируем позицию текста с позицией кнопки
        
        # Рисуем текстовое изображение на экране в указанной позиции
        self.screen.blit(self.msg_image, self.msg_image_rect)