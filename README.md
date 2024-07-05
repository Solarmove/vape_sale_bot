
# Руководство по настройке бота

Это руководство предоставляет пошаговые инструкции по настройке бота на сервере Ubuntu, используя Python 3.12, PostgreSQL и Redis.

## Необходимые компоненты

1. Сервер Ubuntu
2. Python версии 3.11 или 3.12
3. PostgreSQL
4. Redis

## Инструкция по настройке

### Шаг 1: Подготовка среды

- Создайте директорию на сервере Ubuntu для файлов бота:
  ```
  mkdir /path/to/your/bot
  cd /path/to/your/bot
  ```

- Загрузите все необходимые файлы бота в эту директорию.

### Шаг 2: Установка Python и виртуальной среды

- Установите Python 3.12 (если он еще не установлен):
  ```
  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install python3.12 python3.12-venv
  ```

- Создайте и активируйте виртуальную среду:
  ```
  python3.12 -m venv venv
  source venv/bin/activate
  ```

- Установите все зависимости из файла `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

### Шаг 3: Установка и настройка Redis

- Установите Redis:
  Установить по примеру с [оф.сайта](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/
)
### Шаг 4: Установка и настройка PostgreSQL

- Установите PostgreSQL:
  ```
  sudo apt install postgresql postgresql-contrib
  ```

- Создайте новую базу данных и пользователя:
  ```
  sudo -u postgres psql
  CREATE DATABASE your_db_name;
  CREATE USER your_user WITH ENCRYPTED PASSWORD 'your_password';
  GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
  \q
  ```

### Шаг 5: Настройка файла .env

- Отредактируйте файл `.env` с учетными данными базы данных и другими настройками, специфичными для вашего окружения.
Так же нужно добавить апи ключи к платежке NowPayments.io

### Шаг 6: Создание файла сервиса

- Создайте файл systemd service для управления ботом:
  ```ini
  [Unit]
  Description=Телеграм бот (может быть любое название)
  After=network.target

  [Service]
  User=root
  WorkingDirectory=/path/to/your/bot
  ExecStart=/path/to/your/bot/venv/bin/python -m bot
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

- Включите и запустите сервис:
  ```
  sudo systemctl enable bot.service
  sudo systemctl start bot.service
  ```

## Запуск бота

Теперь бот будет работать как сервис и автоматически перезапускаться в случае сбоя. Проверить статус бота можно командой:
```
sudo systemctl status bot.service
```

## Логи бота 

Для просмотра логов можно воспользоваться командой 
### Все логи
```
journalctl -u <service_name.service> 
```

### Логи в реальном времени

```
journalctl -u <service_name.service> -f
```

### Последних n логов
В примере последние 200 логов
```
journalctl -u <service_name.service> -n 200
```

### По времени

```
journalctl -u <service_name.service> --since today

journalctl -u <service_name.service> --since yesterday

journalctl -u <service_name.service> --since 09:00 --until "1 hour ago"
```
