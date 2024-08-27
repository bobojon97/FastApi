# Используем официальный образ Node.js
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package.json package-lock.json /app/

# Устанавливаем зависимости
RUN npm install

# Копируем код React
COPY . /app/

# Запускаем сервер разработки React
CMD ["npm", "start"]