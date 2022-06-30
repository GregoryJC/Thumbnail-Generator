Author: Zhonghai (Gregory) Zhang
Email: Zhonghai.Gregory.Zhang@hotmail.com

1. How to run: 
in
gunicorn server:app -k gevent --access-logfile=logs/thumbnail_generator.log --error-logfile=logs/server_gunicorn.log --timeout 120  -b :630 -w 3

This app should be run in a multi-process way, but if you need to run a single process, enter command: 
python3 server.py


1. How to test: 
	1) Requesting with an image file:
		python3 test_image_file.py

	2) Requesting with an image string:
		python3 test_image_string.py

	3) Requesting with an image url:
		python3 test_image_url.py

3. API URL: http://0.0.0.0:630/generate_thumbnail

4. Request type: POST

5. Headers:
{
	'Content-type': 'application/json', 
	'Accept': 'text/plain'
}

7. Request example:
{
	'image_data': '/9j/4AAQS......QhSh//Z'
}

8. Response example:
{
    'code': 1,
    'message': 'SUCCESS',
    'image_data': '/9j/4AAQS......QhSh//Z'
}


What API endpoints are available and how to use them - It should be easy to run and use the service. Please provide example images, curl requests, etc.


An explanation of your architecture, e.g. What components exist in the system? How are they connected?, What libraries /dependencies/tools did you choose and why?


Any improvements you could make to the service or tests that go beyond the scope of the assignment - e.g. What would need to change to put your service into production? How could it be scaled up or down? How will it handle a high load of requests? What can you do to monitor and manage your services ?
