import sys  # Для выхода из программы
import pygame  # Основная библиотека для создания игры
from time import sleep  # Для создания пауз в игре
from settings import Settings  # Настройки игры
from game_stats import GameStats  # Статистика (очки, жизни)
from scoreboard import Scoreboard  # Отображение счета на экране
from button import Button  # Кнопка Play
from ship import Ship  # Корабль игрока
from bullet import AnimatedBullet  # Анимированные пули
from alien import Alien  # Враги
from background import Background  # Фон игрового процесса
from start_screen_background import StartScreenBackground  # Фон стартового экрана


class AlienInvasion:
    """Класс для управления игрой."""
    # Основной класс, который объединяет все компоненты игры
    
    def __init__(self):
        """Инициализирует игровые ресурсы."""
        pygame.init()  # Инициализация всех модулей Pygame

        # Игра запускается в неактивном состоянии
        self.game_active = False  # Флаг: True - игра идет, False - стартовый экран

        pygame.mixer.init()  # Инициализация звукового модуля
        self.clock = pygame.time.Clock()  # Создание таймера для контроля частоты
        self.settings = Settings()  # Загрузка всех настроек игры

        # Создание окна в полноэкранном режиме
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Обновляем настройки под реальный размер экрана
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")  # Заголовок окна

        # Создание экземпляра для хранения игровой статистики и панели результатов
        self.stats = GameStats(self)  # Хранит очки, жизни, уровень
        self.sb = Scoreboard(self)  # Отображает статистику на экране

        # Создание игровых объектов
        self.ship = Ship(self)  # Корабль игрока
        self.bullets = pygame.sprite.Group()  # Группа для хранения всех пуль
        self.background = Background(self)  # Анимированный фон
        self.aliens = pygame.sprite.Group()  # Группа для хранения всех пришельцев

        self._create_fleet()  # Создание начального флота пришельцев

        # Загрузка и настройка музыки
        self._load_music()

        # Управление звуком
        self.music_playing = False  # Флаг: играет ли музыка

        # Создание кнопки Play
        self.play_button = Button(self, "Play")

        # Анимированный фон стартового экрана
        self.start_screen_bg = StartScreenBackground(self)
        
        # Таймеры для стартового экрана
        self.inactivity_timer = 0  # Таймер бездействия (показывает подсказку)
        self.text_blink_timer = 0  # Таймер для мигания текста
        self.text_visible = True  # Видимость мигающего текста
        
        
    def _create_fleet(self):
        """Создание флота пришельцев."""
        # Создание пришельца для получения его размеров
        alien = Alien(self, x=0, y=0) 
        alien_width, alien_height = alien.rect.size  # Получаем ширину и высоту пришельца

        # Начальные позиции для размещения флота
        current_x = alien_width  # Начальная позиция X
        current_y = 120  # Начальная позиция Y (отступ сверху)
        
        # Внешний цикл: создание рядов (по вертикали)
        while current_y < (self.settings.screen_height - 2 * alien_height):
            # Внутренний цикл: создание пришельцев в ряду (по горизонтали)
            while current_x < (self.settings.screen_width - 1.5 * alien_width):
                self._create_alien(current_x, current_y)  # Создание одного пришельца
                current_x += 1.5 * alien_width  # Сдвиг для следующего пришельца

            # Конец ряда: сбрасываем значение x и инкрементируем (увеличиваем) y
            current_x = alien_width
            current_y += 1.5 * alien_height  # Переход на следующий ряд

    def _create_alien(self, x_position, y_position):
        """Создает пришельца и размещает его в ряду"""
        new_alien = Alien(self, x=x_position, y=y_position)  # Создание пришельца
        self.aliens.add(new_alien)  # Добавление в группу пришельцев

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана, с последующим обновлением
        позиций всех пришельцев во флоте.
        """
        self._check_fleet_edges()  # Проверка достижения края
        self.aliens.update()  # Обновление всех пришельцев

        # Проверка коллизий (касаются ли объекты друг друга) "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()  # Обработка столкновения
        
        # Проверить, сталкиваются ли пришельцы с нижним краем экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцем."""
        if self.stats.ship_left > 0:  # Если еще есть жизни
            # Уменьшение ships_left и обновление панели счета
            self.stats.ship_left -= 1
            self.sb.prep_ships()  # Обновление отображения жизней

            # Очистка групп aliens и bullets
            self.aliens.empty()  # Удаление всех пришельцев
            self.bullets.empty()  # Удаление всех пуль

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза для обратной связи игроку
            sleep(0.1)
        else:
            self.game_active = False  # Конец игры

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        for alien in self.aliens.sprites():  # Для каждого пришельца
            if alien.rect.bottom >= self.settings.screen_height:  # Если достиг нижнего края
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break  # Выход из цикла после первого обнаружения

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():  # Если пришелец у края
                self._change_fleet_direction()  # Меняем направление всего флота
                break  # Достаточно одного пришельца у края

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет его направление."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # Опускаем всех
        self.settings.fleet_direction *= -1  # Меняем направление (1 -> -1 или -1 -> 1)

    def _load_music(self):
        """Загружает и настраивает фоновую музыку."""
        try:
            pygame.mixer.music.load(self.settings.music_path)  # Загрузка файла
            pygame.mixer.music.set_volume(self.settings.music_volume)  # Установка громкости
            print("Музыка загружена успешно")
        except:
            print(f"Не удалось загрузить музыку: {self.settings.music_path}")

    def play_music(self):
        """Запускает фоновую музыку."""
        if not self.music_playing:  # Если музыка не играет
            pygame.mixer.music.play(-1)  # то запустить её(-1 означает бесконечное повторение фоновой музыки)
            self.music_playing = True #и отметить, что теперь играет
            print("Музыка запущена")

    def stop_music(self):
        """Останавливает фоновую музыку."""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            print("Музыка остановлена")

    def set_music_volume(self, volume):
        """Устанавливает громкость музыки."""
        volume = max(0.0, min(1.0, volume))  # Ограничение от 0.0 до 1.0
        self.settings.music_volume = volume  # Сохраняем в настройках
        pygame.mixer.music.set_volume(volume)  # Применяем
        print(f"Громкость музыки установлена: {volume}")  

    def increase_volume(self, amount=0.1):
        """Увеличивает громкость музыки."""
        new_volume = min(1.0, self.settings.music_volume + amount)  # Не более 1.0
        self.set_music_volume(new_volume)

    def decrease_volume(self, amount=0.1):
        """Уменьшает громкость музыки."""
        new_volume = max(0.0, self.settings.music_volume - amount)  # Не менее 0.0
        self.set_music_volume(new_volume)

    def toggle_music(self):
        """Включает/выключает музыку."""
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music()

    def run_game(self):
        """Запускает основной цикл игры."""
        # Автоматически запускает музыку во время игры
        self.play_music()
        
        while True:  # Главный игровой цикл
            self._check_events()  # Проверка событий (клавиши, мышь)

            if self.game_active:  # Если игра активна
                # Обновление всех игровых объектов
                self.ship.update()  # Обновление позиции корабля
                self._update_bullets()  # Обновление пуль
                self._update_aliens()  # Обновление пришельцев
                self.background.update()  # Обновление анимации фона
                self.sb.update_animation()  # Обновление анимации жизней
            else:
                # Обновление стартового экрана
                self._update_start_screen()
            
            self._update_screen()  # Отрисовка всего на экране
            self.clock.tick(60)  # Регулятор скорости игры (60 FPS)

    def _update_start_screen(self):
        """Обновляет логику стартового экрана."""
        # Обновляется анимация фона
        self.start_screen_bg.update()
        
        # Таймер бездействия (в секундах)
        self.inactivity_timer += 1/60  # таймер, который считает секунды бездействия игрока на стартовом экране
        
        # Таймер мигания текста (в кадрах)
        self.text_blink_timer += 1
        if self.text_blink_timer >= self.settings.start_screen_text_blink_interval:
            self.text_blink_timer = 0
            self.text_visible = not self.text_visible  # Переключение видимости

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():  # Для каждого события в очереди
            if event.type == pygame.QUIT:  # Если нажали крестик окна
                sys.exit()  # Выход из игры
            elif event.type == pygame.KEYDOWN:  # Если нажата клавиша
                self._check_keydown_events(event)  # Обработка нажатия
            elif event.type == pygame.KEYUP:  # Если отпущена клавиша
                self._check_keyup_events(event)  # Обработка отпускания

    def _start_game(self):
        """Запускает новую игру."""
        # Сброс игровой статистики
        self.stats.reset_stats()  # Очки, жизни, уровень
        self.sb.prep_score()  # Подготовка отображения счета
        self.sb.prep_level()  # Подготовка отображения уровня
        self.sb.prep_ships()  # Подготовка отображения жизней
        self.game_active = True  # Активация игрового режима

        # Сброс настроек скорости игры к начальным
        self.settings.initialize_dynamic_settings()
        
        # Очистка пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()
        
        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_d:  # D - движение вправо
            self.ship.moving_right = True
        elif event.key == pygame.K_a:  # A - движение влево
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:  # ESC - выход
            sys.exit()
        elif event.key == pygame.K_SPACE:  # ПРОБЕЛ
            if self.game_active:
                self._fire_bullet()  # Стрельба в игре
            else:
                # Запуск игры при нажатии пробела, если игра неактивна
                self._start_game()

        # Управление музыкой
        elif event.key == pygame.K_m:  # M - вкл/выкл музыки
            self.toggle_music()
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # + - громче
            self.increase_volume()
        elif event.key == pygame.K_MINUS:  # - - тише
            self.decrease_volume()
        elif event.key == pygame.K_q:  # Q - полная тишина
            self.set_music_volume(0.0)
        elif event.key == pygame.K_9:  # 9 - почти максимальная громкость
            self.set_music_volume(0.9)

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_d:  # Отпустили D
            self.ship.moving_right = False
        elif event.key == pygame.K_a:  # Отпустили A
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создает новый снаряд и добавляет в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:  # Ограничение на количество пуль
            new_bullet = AnimatedBullet(self)  # Создание пули
            self.bullets.add(new_bullet)  # Добавление в группу

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        self.bullets.update()  # Обновление всех пуль

        # Удаление пуль, вылетевших за верх экрана
        for bullet in self.bullets.copy():  # Копия списка для безопасного удаления
            if bullet.rect.bottom <= 0:  # Если пуля выше верхней границы
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()  # Проверка столкновений

    def _check_bullet_alien_collisions(self):
        """Обрабатывает коллизии снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях
        # groupcollide - это функция, которая проверяет ВСЕ пули против ВСЕХ пришельцев сразу
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)  # True, True - удалять оба объекта при столкновении
        
        if collisions:  # Если были столкновения
            for aliens in collisions.values():  # Для каждой группы сбитых пришельцев
                # Начисление очков: очки за пришельца × количество_сбитых
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()  # Обновление отображения счета
            self.check_high_score()  # Проверка рекорда

        # Если все пришельцы уничтожены
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()  # Увеличение скорости игры

            # Увеличение уровня  
            self.stats.level += 1
            self.sb.prep_level()  # Обновление отображения уровня

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score  # Обновление рекорда
            self.sb.prep_high_score()  # Обновление отображения рекорда

    def _draw_start_screen_text(self):
        """Рисует мигающую надпись на стартовом экране."""
        font = pygame.font.SysFont(None, 30)  # Шрифт размера 30
        text = font.render("Для начала игры нажмите пробел", True, (255, 255, 255))  # Белый текст
        text_rect = text.get_rect(center=(self.settings.start_screen_text_x, 
                                     self.settings.start_screen_text_y))  # Центрирование
        self.screen.blit(text, text_rect)  # Отрисовка текста

    def _update_screen(self):
        """Отрисовывает все объекты на экране."""
        if self.game_active:  # Если игра активна
            # Игровой экран
            self.background.draw()  # Фон
            for bullet in self.bullets.sprites():  # Все пули
                bullet.draw_bullet()
            self.ship.blitme()  # Корабль
            self.aliens.draw(self.screen)  # Все пришельцы
            self.sb.show_score()  # Статистика (очки, жизни, уровень)
        else:
            # Стартовый экран с анимированным фоном
            self.start_screen_bg.draw()  # Фон стартового экрана
            self.play_button.draw_button()  # Кнопка Play
            
            # Отображается мигающий текст после 15 секунд бездействия
            if self.inactivity_timer >= self.settings.start_screen_inactivity_time and self.text_visible:
                self._draw_start_screen_text()

        pygame.display.flip()  # Обновление всего экрана

if __name__ == '__main__':  # Если файл запущен напрямую, то код выполняется
    ai = AlienInvasion()  # Создание объекта игры
    ai.run_game()  # Запуск игрового цикла