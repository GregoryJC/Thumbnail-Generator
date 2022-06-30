Author:	Zhonghai (Gregory) Zhang  
Email:	Zhonghai.Gregory.Zhang@hotmail.com

1. This API is able to:
	- Resize an image from an image file.
	- Resize an image from an image base64 string.
	- Resize an image from an image URL.  
	- And image can be jpg/jpeg/png/bmp. 
  
2. How to run:  
	(in the current folder)
	```
	sudo docker-compose up
	```
	This api will automatically run in a multi-process way after running ```sudo docker-compose up```, as written in run.sh: 
	```
	/usr/local/bin/gunicorn server:app -k gevent --access-logfile=logs/thumbnail_generator.log --error-logfile=logs/server_gunicorn.log --timeout 120  -b :630 -w 3
	```  
	But if you need to run a single process, enter the conainer 
	```
	sudo docker exec -it {the_container_id} /bin/bash
	```
	then enter command: 
	```
	python3 server.py
	```

3. How to test:   
   There are 3 testing files:
	- Request with an image file:  
		```
		python3 test_image_file.py
		```

	- Request with an image base64 string:  
		```
		python3 test_image_string.py
		```

	- Request with an image url:  
		```
		python3 test_image_url.py
		```

	If you are running on Linux OS and see messages like this:  
	```
	Error: no "view" rule for type "image/png" passed its test case
	(for more information, add "--debug=1" on the command line)
	/usr/bin/xdg-open: 882: www-browser: not found
	/usr/bin/xdg-open: 882: links2: not found
	/usr/bin/xdg-open: 882: elinks: not found
	```
	or this: 
	```
	display-im6.q16: unable to open X server `' @ error/display.c/DisplayImageCommand/412.
	```
	It means the api works well, but there is no available tool to display the image on your screen. 

4. API documentation:
   - API URL:	http://0.0.0.0:630/generate_thumbnail

   - Request type: POST

   - Headers:
		```
		{
			'Content-type': 'application/json', 
			'Accept': 'text/plain'
		}
		```

   - Request example:
		```
		{
			'image_data': '/9j/4AAQS......QhSh//Z'
		}
		```

   - Response example:
		```
		{
			'code': 1,
			'message': 'SUCCESS',
			'image_data': '/9j/4AAQSk......04JWs'
		}
		```

5. libraries used:
	- Flask==2.0.1		(backend framework)
	- Pillow==9.1.1		(tool for image processing)
	- requests==2.26.0	(tool to download image by url)
	- gunicorn==20.1.0	(starts multi-processing API)
	- gevent==21.12.0	(provides a high-level synchronous API)

6. Notes:  
	Unfortunately, I just caught up with the very important semi-annual report recently, and I have two projects to catch up with, so I don't have enough time to develop this project to the state I want.

	If I could spare another day, I would use redis as cache and RabbitMQ as a message queue.

	Technologies currently in this project include:
	- Local cache: Repeated tasks (whether image files, base64 strings or URLs) can get the processing results directly from the local, which will normally take less than 50ms.   
	- Multi-process: The default number of multi-processes is 3. If there is a high load of requests, the number of processes can be increased.

