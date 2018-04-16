# Fake News Detector
> Fake News Detector, composed of Android App and Cloud (server-side) API to recognize fake news. The API exploits a Naive Bayesian Network for the recognition of the news, training is done using user's input from the andoid app.

## Start the server
To start the server, execute the following commands in the console (these are contained into the launc_server.bat file). Server is run on local machine using Flask module for Python. 
```
set FLASK_APP=api.py
python -m flask run
```
This way, the data of the domains are available **on your machine** at:

```
0.0.0.0:5000/domains
```
in a JSON format, containing all the websites with most important data;
```
0.0.0.0:5000/domains/<url>
```
where <url> is the website you want full information about (still in JSON);

```
0.0.0.0:5000/domains/urls/all
```
obtains all the information regarding all the websites (still in JSON).

#### Locally Available Server

If you wish to access the server from your local network, you need to run these instructions instead
```
set FLASK_APP=api.py
flask run --host=0.0.0.0
```
This way you will access the data by pointing to your local ip (can be seen running the command **ipconfig** within the console), for example:
```
10.100.19.59:500/domains
```

## Reference
Fake News Detector makes use of Python module **newspaper**.

