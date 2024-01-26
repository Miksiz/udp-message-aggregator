# Прием и аггрегация данных UDP-сообщениий
Программа запускает сервер, который слушает UDP запросы на заданном порте и пишет в файл out.txt результаты аггрегации данных
Данная программа реализована в рамках тестового задания, текст которого расположен в фале [test.py](test.py)
Результаты записываются в файл out.log в рабочей директории

## Запуск под Linux
Запускать с помощью python версии не ниже 3.7, указав в аргументах номер порта
Остановка программы по сочетанию клавиш Ctrl+C
```
python3 main.py 8000
```
Проверить работоспособность можно используя модуль sender в параллельно открытом терминале, порт задается в файле settings.py
```
python3 sender.py
```