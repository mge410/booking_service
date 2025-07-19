# booking_service

Сервис представляет собой простой механизм бронирования комнат отеля.

Есть всего несколько endpoint'ов  

Список комнат ``GET`` ```/api/v1/room?ordering=created_at```  
Создание комнаты ``POST`` ```/api/v1/room/```  
Удаление комнаты и всех записей связанных с ней ``DELETE`` ```/api/v1/room/{room_id}```

Список броней для конкретной комнаты ``GET`` ```/api/v1/booking/?room={room_id}```  
Создание бронь ``POST`` ```/api/v1/booking/```  
Удаление брони ``DELETE`` ```/api/v1/booking/{booking_id }```


Инструкция для развертки проекта:  
Проект разворачивается при помощи docker.

1. Копируем .env.example и создаём файл .env
2. Запускаем docker-compose up -d
3. На http://localhost:8000 будет проект
