@echo off
cd /d %~dp0

echo 📁 Переход в папку с ботом: %cd%

echo.
echo 🔍 Проверка статуса...
git status

echo.
echo ➕ Добавление всех изменений...
git add .

echo.
set /p msg=💬 Введите комментарий для коммита: 
git commit -m "%msg%"

echo.
echo 🚀 Отправка в репозиторий...
git push origin main

echo.
echo ✅ Репозиторий обновлён!
pause
