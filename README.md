# Руководство по настройке бота

Это руководство предоставляет пошаговые инструкции по настройке бота на сервере Ubuntu с использованием Docker и Docker Compose.

## Необходимые компоненты

1. Сервер Ubuntu
2. Docker
3. Docker Compose

## Установка Docker и Docker Compose

1. Установите докер
   согласно [гайду](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru)
2. Установите Docker Compose
   согласно [гайду](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru)

## Добавление пользователя в группу Docker

### Добавьте пользователя в группу Docker

  ```bash 
  sudo usermod -aG docker $USER
  ```

### Перезапустите сеанс пользователя для применения изменений:

Вы можете выйти и войти в систему заново, либо выполнить следующую команду:

```bash 
su - $USER
 ```

## Настройка бота

Перейдите в директорию с ботом и переименуйте файл `.env.example` на `.env` и заполните пустые переменные данными.

## Запуск бота

Предполагая, что у вас уже есть файл docker-compose.yml в вашей рабочей директории, выполните следующие шаги для запуска контейнеров:

1. Перейдите в директорию с вашим Docker Compose файлом:
   ```bash
   cd /path/to/your/directory
2. Запустите Docker Compose:
   ```bash
   docker-compose up -d
   ```
Флаг -d запускает контейнеры в фоновом режиме (detached mode). Если вы хотите увидеть логи контейнеров в реальном времени, запустите без флага -d:


## Полезные команды Docker Compose
1. Остановить все запущенные контейнеры:
   
   ```bash
   docker-compose down

2. Перезапустить контейнеры:
   ```bash
   docker-compose restart
3. Просмотреть логи:
    ```bash
   docker-compose logs
4. Просмотреть статус контейнеров:
    ```bash
    docker-compose ps