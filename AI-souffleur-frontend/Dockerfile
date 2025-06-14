# Установим Node.js
FROM node:20-alpine

# Установим рабочую директорию
WORKDIR /app

# Скопируем package.json и lock-файл
COPY package*.json ./

# Установим зависимости
RUN npm install

# Копируем остальные файлы проекта
COPY . .

# Соберем проект
RUN npm run build

# Установим сервер для отдачи статики
RUN npm install -g serve

# Запускаем приложение на порту 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
