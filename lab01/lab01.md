# Практика 1. Wireshark: HTTP
Эта работа исследует несколько аспектов протокола HTTP: базовое взаимодействие GET/ответ,
форматы сообщений HTTP, получение больших файлов HTML, получение файлов HTML со
встроенными объектами, а также проверку подлинности и безопасность HTTP.

Во всех заданиях (а также во всех следующих лабах) предполагается, что вы к своему ответу 
приложите **подтверждающий скрин** программы Wireshark (достаточно одного скрина на задание).

## Задание 1. Базовое взаимодействие HTTP GET/response (2 балла)

#### Подготовка
1. Запустите веб-браузер.
2. Запустите анализатор пакетов Wireshark, но пока не начинайте захват пакетов. Введите
   «http» в окне фильтра, чтобы позже в окне списка пакетов отображались только захваченные сообщения HTTP.
3. Подождите несколько секунд, а затем начните захват пакетов Wireshark.
4. Введите в браузере адрес: http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html.  
   Ваш браузер должен отобразить очень простой однострочный HTML-файл.
5. Остановите захват пакетов Wireshark.

<img width="1920" height="1040" alt="image" src="https://github.com/user-attachments/assets/78550c09-afa0-42c5-b4bc-f58520e821f6" />


#### Вопросы
1. Использует ли ваш браузер HTTP версии 1.0 или 1.1? Какая версия HTTP работает на
   сервере?
   
   - <img width="186" height="22" alt="image" src="https://github.com/user-attachments/assets/f3421df7-6eee-41b1-895e-82274962fce5" />
   
   - <img width="195" height="20" alt="image" src="https://github.com/user-attachments/assets/08e6dd75-bd97-4ece-829b-265625e93d0a" />

2. Какие языки (если есть) ваш браузер может принимать? В захваченном сеансе какую еще
   информацию (если есть) браузер предоставляет серверу относительно пользователя/браузера?
   
   - <img width="236" height="21" alt="image" src="https://github.com/user-attachments/assets/0965746f-8d8f-4473-bdca-135030a2773f" />

   - <img width="1041" height="19" alt="image" src="https://github.com/user-attachments/assets/d94aa045-e353-470c-b865-28d7635e1dc3" />
      Видим информацию об ОС и том, какой браузер используется.

3. Какой IP-адрес вашего компьютера? Какой адрес сервера gaia.cs.umass.edu?
   
   Для GET запроса:
   - <img width="206" height="18" alt="image" src="https://github.com/user-attachments/assets/bb185c03-5148-4812-b5cb-6d2cd165a5e9" />

   - <img width="254" height="18" alt="image" src="https://github.com/user-attachments/assets/6125de91-e020-45d3-b53b-2325098c8ad7" />

4. Какой код состояния возвращается с сервера на ваш браузер?

   - <img width="122" height="20" alt="image" src="https://github.com/user-attachments/assets/7fe41f3a-098a-4aa1-bc92-c6516587a05e" />

5. Когда HTML-файл, который вы извлекаете, последний раз модифицировался на сервере?

   - <img width="349" height="20" alt="image" src="https://github.com/user-attachments/assets/a7133ca7-5a9e-4cbd-89cf-10dc740d219a" />

6. Сколько байтов контента возвращается вашему браузеру?
   
   - <img width="202" height="34" alt="image" src="https://github.com/user-attachments/assets/da61dd8f-aa77-461a-8981-65aebcab141c" />

## Задание 2. HTTP CONDITIONAL GET/response (2 балла)
Большинство веб-браузеров выполняют кэширование объектов и, таким образом, выполняют
условный GET при извлечении объекта HTTP. Прежде чем выполнять описанные ниже шаги, 
убедитесь, что кеш вашего браузера пуст.


#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html.  
   Ваш браузер должен отобразить очень простой пятистрочный HTML-файл.
4. Введите тот же URL-адрес в браузер еще раз (или просто нажмите кнопку обновления в
   браузере).
5. Остановите захват пакетов Wireshark и введите «http» в окне фильтра, чтобы в окне списка
   пакетов отображались только захваченные HTTP-сообщения.

<img width="1920" height="1040" alt="image" src="https://github.com/user-attachments/assets/a3fe037f-81f6-45fa-b955-797128fb7702" />

#### Вопросы
1. Проверьте содержимое первого HTTP-запроса GET. Видите ли вы строку «IF-MODIFIED-SINCE» в HTTP GET?
   - Нет, это обычный запрос, т.к. кэш пуст
2. Проверьте содержимое ответа сервера. Вернул ли сервер содержимое файла явно? Как вы
   это можете увидеть?
   
   - Да
   
   - <img width="658" height="193" alt="image" src="https://github.com/user-attachments/assets/949897bf-ccd4-4a3f-8fb0-7c7e1b7b62a5" />

3. Теперь проверьте содержимое второго HTTP-запроса GET (из вашего браузера на сторону
   сервера). Видите ли вы строку «IF-MODIFIED-SINCE» в HTTP GET? Если да, то какая
   информация следует за заголовком «IF-MODIFIED-SINCE»?

   - <img width="370" height="22" alt="image" src="https://github.com/user-attachments/assets/3885ad45-557e-4da3-8a00-6226d58790f3" />

4. Какой код состояния HTTP и фраза возвращаются сервером в ответ на этот второй запрос
   HTTP GET? Вернул ли сервер явно содержимое файла?

   - <img width="292" height="51" alt="image" src="https://github.com/user-attachments/assets/6faccfe9-a47c-472d-a5b6-19d87b3e10a6" />

   - Нет, т.к. файл не изменился

## Задание 3. Получение длинных документов (2 балла)

#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html  
   В браузере должен отобразиться довольно длинный текст.
4. Остановите захват пакетов Wireshark и введите «http» в окне фильтра.

<img width="1920" height="1041" alt="image" src="https://github.com/user-attachments/assets/f9645c17-352e-4406-989e-ed7b66056a85" />

#### Вопросы
1. Сколько сообщений HTTP GET отправил ваш браузер? Какой номер пакета в трассировке
   содержит сообщение GET?
   - Один

   - <img width="947" height="37" alt="image" src="https://github.com/user-attachments/assets/7a2c9deb-e1a4-4a3c-8e7b-92e326313c44" />

2. Какой номер пакета в трассировке содержит код состояния и фразу, связанные с ответом
   на HTTP-запрос GET?

   - <img width="949" height="56" alt="image" src="https://github.com/user-attachments/assets/c4268076-06fb-480e-89b6-b5ec9588415a" />

3. Сколько сегментов TCP, содержащих данные, потребовалось для передачи одного HTTP ответа?

   Помимо самого HTTP ответа было еще 3 TCP сегмента для передачи ответа
   
   - <img width="1069" height="138" alt="image" src="https://github.com/user-attachments/assets/e0d9c843-5d13-4cf3-a648-bf807bd0e3d9" />

4. Есть ли в передаваемых данных какая-либо информация заголовка HTTP, связанная с
   сегментацией TCP?

   - Да
   <img width="1054" height="137" alt="image" src="https://github.com/user-attachments/assets/3e9eab01-cac1-41c2-9568-fbb16914ee4d" />

## Задание 4. HTML-документы со встроенными объектами (2 балла)
Исследуйте, что происходит, когда ваш браузер загружает файл со встроенными объектами, т. е. файл, 
включающий в себя другие объекты (в данном примере это файлы и картинки),
которые хранятся на другом сервере (серверах).

#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html.  
   Ваш браузер должен отобразить HTML-файл с двумя изображениями. На эти два изображения есть ссылки в
   базовом файле HTML. То есть сами изображения не содержатся в HTML, вместо этого URL-
   адреса изображений содержатся в загруженном файле HTML. Ваш браузер должен
   получить эти изображения с указанных веб-сайтов.
4. Остановите захват пакетов Wireshark и введите «http» в окне фильтра.

<img width="1920" height="1042" alt="image" src="https://github.com/user-attachments/assets/8ed1e992-20bf-4d68-94c2-9a619ce0b05f" />

#### Вопросы
1. Сколько HTTP GET запросов было отправлено вашим браузером? На какие интернет-адреса были отправлены эти GET-запросы?
   - 3 GET запроса. Из них 2 это запросы картинок:
     <img width="909" height="15" alt="image" src="https://github.com/user-attachments/assets/073912ca-aedb-4e00-8475-0b5200677051" />
     
     <img width="701" height="18" alt="image" src="https://github.com/user-attachments/assets/14606e4d-8a0d-4b42-aa99-9c60cf0239ce" />
     
     <img width="749" height="18" alt="image" src="https://github.com/user-attachments/assets/5fbf475d-668d-4652-833b-3c6720a09c60" />
     
   - <img width="554" height="20" alt="image" src="https://github.com/user-attachments/assets/049a62fd-eda5-4780-a992-e562babeafc8" />
   
     <img width="272" height="17" alt="image" src="https://github.com/user-attachments/assets/279bc831-e557-4d43-a65d-b295a12fbf08" />


2. Можете ли вы сказать, загрузил ли ваш браузер два изображения последовательно или
   они были загружены с веб-сайтов параллельно? Объясните.
   - Последовательно, так как временные метки запросов сильно отличаются. Второй запрос ушел аж через 3 секунды после первого.
     
      <img width="675" height="15" alt="image" src="https://github.com/user-attachments/assets/221b93ef-b37f-4140-9fd1-849cac452716" />

      <img width="721" height="16" alt="image" src="https://github.com/user-attachments/assets/342d20b5-0fd2-4059-8a31-3d94828701d9" />

## Задание 5. HTTP-аутентификация (2 балла)
Запустите веб-сайт, защищенный паролем, и исследуйте последовательность HTTP-сообщений, которыми обмениваются такие сайты.

#### Подготовка
1. Убедитесь, что кеш вашего браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html
4. Введите требуемые имя пользователя и пароль во всплывающем окне  
   (Имя пользователя — «wireshark-students», пароль — «network»).
5. Остановите захват пакетов Wireshark и введите «http» в окне фильтра

<img width="1920" height="1041" alt="image" src="https://github.com/user-attachments/assets/a36b6053-fe48-488f-9b7c-915c0edc2851" />

#### Вопросы
1. Каков ответ сервера (код состояния и фраза) в ответ на начальное HTTP-сообщение GET от вашего браузера?

   - <img width="277" height="52" alt="image" src="https://github.com/user-attachments/assets/ff2a3a1b-b9f8-45bf-a7eb-5bfb547206a0" />

2. Когда ваш браузер отправляет сообщение HTTP GET во второй раз, какое новое поле включается в сообщение HTTP GET?

   - Метод кодирования и сам логин и пароль для авторизации
   
     <img width="438" height="35" alt="image" src="https://github.com/user-attachments/assets/e694d572-fc69-4c10-adb2-0ec333e19957" />
