import pygame
import random
import time

# Инициализация PyGame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
TOTAL_TIME = 60  # время игры в секундах
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # Коричневый цвет для земли
SKY_BLUE = (135, 206, 235)  # Голубой цвет для неба
DARK_BLUE = (0, 0, 139)  # Темно-синий для верха неба

# Путь к шрифту Minecraft (убедитесь, что файл шрифта находится в той же директории, что и ваш код)
MINECRAFT_FONT_PATH = 'rsc/minecraft.ttf'  # Поменяйте на имя вашего шрифта
FONT_SIZE = 30
SMALL_FONT_SIZE = 20

# Текстуры для деревьев
CACTUSES_TEXTURES = ['rsc/cactus.jpg', 'rsc/cactus.png', 'rsc/cactus.webp']  # Список с текстурами деревьев

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Математическая лестница")

# Игровые переменные
score = 0
input_answer = ''
current_answer = None
current_question = ""
game_over = False
clock = pygame.time.Clock()

# Таймер
start_ticks = pygame.time.get_ticks()  # время начала игры

# Рекорд
max_score = 0

# Список деревьев (каждое дерево будет состоять из нескольких сегментов)
cactuses = []


# Функция для генерации математических примеров (без деления)
def generate_question():
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)

    # num1 = random.randint(0, 0)
    # num2 = random.randint(0, 0)
    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = num1 + num2
    elif operation == "-":
        answer = num1 - num2
    elif operation == "*":
        answer = num1 * num2

    return f"{num1} {operation} {num2}", answer


# Генерируем первый пример перед началом игры
current_question, current_answer = generate_question()


# Функция для рисования текста на экране
def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Функция для проверки, не пересекается ли новое дерево с существующими
def is_valid_position(new_cactuses, cactuses, min_distance=50):
    for cactus in cactuses:
        # Проверяем, что новое дерево не перекрывает существующие деревья
        if abs(new_cactuses['x'] - cactus['x']) < min_distance:
            return False
    return True


# Функция для загрузки случайной текстуры дерева
def get_random_cactuses_segment_image():
    cactus_texture = random.choice(CACTUSES_TEXTURES)  # Выбираем случайную текстуру из списка
    cactus_img = pygame.image.load(cactus_texture)  # Загружаем выбранную текстуру дерева
    cactus_img = pygame.transform.scale(cactus_img, (50, 50))  # Масштабируем изображение сегмента дерева в квадрат
    return cactus_img


# Функция для отрисовки текстуры земли, чтобы она повторялась по всему экрану
def draw_ground_texture():
    ground_img = pygame.image.load('rsc/sand.jpg')  # Загружаем текстуру земли
    ground_img = pygame.transform.scale(ground_img, (50, 50))  # Масштабируем текстуру земли под блоки
    for i in range(0, WIDTH, 50):  # Рисуем землю по ширине экрана
        screen.blit(ground_img, (i, HEIGHT - 50))


# Загрузка шрифтов
font = pygame.font.Font(MINECRAFT_FONT_PATH, FONT_SIZE)  # Шрифт для интерфейса
small_font = pygame.font.Font(MINECRAFT_FONT_PATH, SMALL_FONT_SIZE)  # Меньший шрифт для подсказок


# Главный игровой цикл
new_cactus_surface = None
while True:
    screen.fill(WHITE)

    # Рисуем фон
    screen.blit(pygame.image.load('rsc/sky.webp'), (0, 0))  # Используем sky.webp для фона

    # Расчёт оставшегося времени
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    remaining_time = max(0, TOTAL_TIME - elapsed_time)

    # Если время истекло, завершаем игру
    if remaining_time <= 0:
        game_over = True

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:
                # Проверка, является ли ввод числом
                if input_answer.lstrip('-').isdigit():
                    if int(input_answer) == current_answer:
                        # При верном ответе добавляем новый сегмент дерева
                        if len(cactuses) == 0:  # Если деревьев нет, создаем первое дерево
                            cactuses_x = random.randint(50, WIDTH - 50)
                            cactuses_texture = get_random_cactuses_segment_image()  # Выбираем текстуру дерева для всего дерева
                            cactuses.append({'x': cactuses_x, 'y': HEIGHT - 50, 'segments': [cactuses_texture]})
                        else:
                            # Добавляем новый сегмент дерева

                            cactuses[-1]['segments'].append(new_cactus_surface if new_cactus_surface is not None else cactuses_texture)
                        score += 1
                    else:
                        # Если ответ неверный, дерево не изменяется
                        pass
                    # Генерация нового примера
                    current_question, current_answer = generate_question()
                    input_answer = ''
                else:
                    # Если введено не число, выводим сообщение и сбрасываем ввод
                    current_question = "Введите число!"
                    input_answer = ''
            elif event.key == pygame.K_BACKSPACE:
                input_answer = input_answer[:-1]
            elif event.key == pygame.K_ESCAPE:
                game_over = True
            else:
                # Принимаем ввод только цифр и минуса
                if event.unicode.isdigit() or (event.unicode == '-' and input_answer == ''):
                    input_answer += event.unicode

        # Если игра закончена
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск игры
                    # Если рекорд побит, показываем сообщение
                    if score > max_score:
                        max_score = score
                        current_question = f"Новый рекорд! {score}"

                    # Сбрасываем значения для новой игры
                    cactuses = []  # Очищаем деревья
                    score = 0
                    input_answer = ''
                    current_question, current_answer = generate_question()
                    start_ticks = pygame.time.get_ticks()  # сбрасываем таймер
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    # Рисуем землю с текстурой, которая повторяется
    draw_ground_texture()

    # Рисуем деревья с текстурой для каждого сегмента
    for cactus in cactuses:
        for i, segment in enumerate(cactus['segments']):
            screen.blit(segment, (cactus['x'], HEIGHT - 50 - (i + 1) * 50))  # Рисуем сегменты дерева, с размером 50x50

    # Проверка, если дерево достигло верхней части экрана, создаем новое дерево на земле
    if cactuses and cactuses[-1]['y'] - len(cactuses[-1]['segments']) * 50 <= 0:  # Если дерево достигло верхней части экрана
        # Пытаемся найти валидную позицию для нового дерева
        new_cactus_surface = get_random_cactuses_segment_image()
        new_cactus = {'x': random.randint(50, WIDTH - 50), 'y': HEIGHT - 50, 'segments': [new_cactus_surface]}
        while not is_valid_position(new_cactus, cactuses):
            # Если позиция не валидна (слишком близко к другому дереву), пробуем снова
            new_cactus['x'] = random.randint(50, WIDTH - 50)
        # Создаем новое дерево в найденной позиции
        cactuses.append(new_cactus)

    # Отображение интерфейса (все элементы интерфейса должны быть сверху)
    # Отображение текущего примера
    draw_text(f"Пример: {current_question}", font, WHITE, 100, 50)

    # Отображение введенного ответа
    draw_text(f"Ваш ответ: {input_answer}", font, WHITE, 100, 100)

    # Отображение текущего счета
    draw_text(f"Счет: {score}", font, WHITE, 100, 150)

    # Отображение таймера
    draw_text(f"Время: {int(remaining_time)} сек", font, WHITE, 400, 50)

    # Отображение рекорда
    draw_text(f"Рекорд: {max_score}", font, WHITE, 400, 100)

    # Если игра окончена, выводим сообщение
    if game_over:
        draw_text(f"Игра окончена! Ваш рекорд: {score}", font, RED, 100, HEIGHT // 2)
        draw_text("Нажмите R для перезапуска или ESC для выхода", small_font, WHITE, 100, HEIGHT // 2 + 40)

    pygame.display.update()
    clock.tick(FPS)
