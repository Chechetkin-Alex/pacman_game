# Что насчет логики? (TL;DR)
Класс *Field* представляет собой игровое поле и имеет методы для работы с ним, а также с находящимися на нём объектами. Поле также содержит константы игры и хранит их в классе *Var*. Объекты, находящиеся на поле, представляют собой абстрактный класс *Being*. Абстрактный класс *Being* имеет поля для хранения координат объекта, констант игры и размера данного объекта. 

Координаты представлены классом *Coord*, который имеет несколько методов для работы с ними, в том числе перевода из одной системы координат в другую. Системы координат у нас три, а именно нормальная, пиксельная и клеточная. В нормальной системе одна координатная единица равна одному шагу игрока или привидения. В пиксельной системе координат одна координатная единица равна одному пикселю. В клеточной системе координат одна координатная единица равна одной клетке поля. Экземпляр класса *Coord* хранит в себе координаты в нормальной системе, а также имеет методы для преобразования этих координат в пиксельную или клеточную систему. 

Кроме того, экземпляр класса *Coord* имеет методы для определения, находятся ли данные координаты по центру одной из клеток поля, а также, для удобства работы, методы для замены координат на новое значение и для сдвига координат в нужном направлении. Также данный класс имеет методы для вычисления расстояния между двумя точками по их координатам, а также для нахождения середины отрезка между двумя точками. Экземпляр данного класса и является отвечающим за координаты полем абстрактного класса Being. 

Класс *Being* является родительским для класса *Point*, представляющего точку на поле, и абстрактного класса *Moving*, представляющего собой движущийся объект. Экземпляр класса *Point*, представляющий точку на поле, помимо полей и методов, унаследованных от класса *Being*, имеет поле для хранения категории данной точки, а также метод для рисования точки на экране. Абстрактный класс *Moving* имеет поля для хранения скорости движущегося объекта, текущего направления движения, а также списка разрешённых на данный момент направлений. Также реализованы методы для установки значений этих трёх полей. 

Кроме того, абстрактный класс *Moving* также содержит метод move, который двигает данный объект на один шаг. Так реализован абстрактный класс *Moving*, и от него наследуется класс *Player*, представляющий игрока, а также класс *Ghost*, представляющий привидение. 

Класс Player, помимо полей и методов, унаследованных от родительского класса, имеет метод установки констант текущего поля и метод перемещения на стартовую позицию, поскольку экземпляр класса *Player* существует до создания поля и при создании поля необходимо разместить данного игрока в нужном месте. Также имеется метод для обработки смены направления игрока при нажатии на клавиши и метод для включения "**angry mode**", и для правильной обработки этих событий также переопределён метод move и созданы несколько дополнительных полей. 

Кроме того, реализованы метод для обработки встречи игрока с привидением и метод для рисования игрока на поле. Так реализован класс *Player*. Класс *Ghost*, представляющий привидение, имеет переопределённый метод установки нового направления для движения, поскольку привидение не может стоять на месте и должно самостоятельно выбирать направление движения в случае неопределённой ситуации. 
Также в классе *Ghost* есть методы для установки "**blind mode**" и "**eaten mode**", и с учётом данных состояний реализованы методы получения скорости и получения цели привидения, куда оно двигается. Также для учёта данных состояний реализован метод рисования привидения на экране, а также переопределён метод move. Кроме того, реализован метод для отправки привидения на стартовую позицию. 

С реализованными объектами работает экземпляр класса *Field*. Он хранит в себе список игроков, привидений и точек, карту поля и его константы. Помимо методов инициализации, класс *Field* имеет методы работы с полем, а именно метод для определения совпадения координат объектов, метод для проверки доступности конкретной клетки и метод для поиска кратчайшего пути от одной клетки до другой.
Далее, класс *Field* имеет методы рисования поля и информационного меню снизу. Рисование информационного меню снизу требует хранения большого количества констант, поэтому их было решено вынести в отдельный класс *InfoDrawer* вместе с методом рисования информационного меню, во избежание захламления класса *Field*. 

Кроме того, класс *Field* содержит метод для обработки одного шага игры и метод для обработки ситуации, когда игрок встречает привидение. Метод, обрабатывающий шаг игры, возвращает значение, обозначающее конец игры или её продолжение. 

Помимо всего вышеперечисленного, экземпляр класса *Field* использует класс *SoundController* для включения звуков в игре. Класс *SoundController*, в свою очередь, берёт звуки из класса *SoundCollection*. Для работы с ними в классе *SoundController* реализованы методы воспроизведения и остановки конкретного звука, установки громкости, а также воспроизведения главной музыки при отсутствии других звуков. Так реализован класс *Field*, отвечающий за игровой процесс. 

Для отображения главного меню написано несколько функций, которые отвечают за различные экраны главного меню. Для удобства работы с ними также реализован класс *Button*, обозначающий кнопку на экране и имеющий методы рисования и проверки, нажата ли она. Функции, рисующие соответствующие экраны, используют этот класс для рисования кнопки на экране. Данные функции вызывают друг друга при переходе от одного меню к другому. Так реализовано главное меню.

# Какие паттерны использовали?
- Класс *Controller* - **singleton** (порождающий) и **observer** (поведенческий)
- Класс *Field* - **facade** (структурный)
- Класс *Point* - **prototype** (порождающий)
- Класс *Player* - **state** (порождающий)

# Комментарии по технической итерации
В связи с растущей долей использования протокола Wayland, использование единственного метода проброса графики между контейнером и клиентским устройством через unix-сокет устарело. Wayland же подобной возможности не предоставляет при сохранении кросслатформенности. 

К сожалению, так, чтобы был вывод изображения и при этом играла музыка, а в довесок всё это работало на macOS, реализовать неполучилось. Ниже прикладываю наброски Dockerfile и логи. 

Dockerfile:
```
FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y install python3-pygame xorg x11-apps xinit alsa-base
RUN mkdir -p /opt/pacman_game
WORKDIR /opt/pacman_game
COPY pacman_game/*.py .
COPY pacman_game/Assets Assets
# RUN adduser tmpUser
# RUN echo 'exec python3 /opt/pacman_game/main.py' > /home/nbah/.xinitrc
# RUN printf '#!/bin/sh\nexec /usr/bin/Xorg -nolisten tcp "$@" vt$XDG_VTNR' > /home/tmpUser/.xserverrc
ENV SDL_VIDEODRIVER=x11
ENV SDL_AUDIODRIVER=disk
ENV DISPLAY=127.0.0.1:0
# RUN touch /opt/pacman_game/sdlaudio.raw && chown tmpUser /opt/pacman_game/sdlaudio.raw
CMD python3 /opt/pacman_game/main.py
```

Logs:
(проблемы со звуком) 

```
chechetkinsasha@MacBook-Air-Aleksandr-3 pacman_game % xQuartz &
chechetkinsasha@MacBook-Air-Aleksandr-3 pacman_game % docker run  -it --network=host --env DISPLAY=127.0.0.1:11.0  --privileged --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/snd:/dev/snd tmpUser
pygame 2.1.2 (SDL 2.0.20, Python 3.10.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
Traceback (most recent call last):
  File "/opt/pacman_game/main.py", line 1, in <module>
    from field import Field
  File "/opt/pacman_game/field.py", line 6, in <module>
    from controller import Controller
  File "/opt/pacman_game/controller.py", line 1, in <module>
    from sounds_collection import SoundsCollection
  File "/opt/pacman_game/sounds_collection.py", line 3, in <module>
    pygame.mixer.init()
pygame.error: Couldn't open sdlaudio.raw
```

(проблемы с картинкой)
```
chechetkinsasha@MacBook-Air-Aleksandr-3 pacman_game % xQuartz &
chechetkinsasha@MacBook-Air-Aleksandr-3 pacman_game % docker run  -it --privileged --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/snd:/dev/snd tmpUser
pygame 2.1.2 (SDL 2.0.20, Python 3.10.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
CRITICAL: You are using the SDL disk i/o audio driver!
CRITICAL:  Writing to file [sdlaudio.raw].
Traceback (most recent call last):
  File "/opt/pacman_game/main.py", line 14, in <module>
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.error: x11 not available
```
