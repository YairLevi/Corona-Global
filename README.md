
# COVID-19 Global Data Displayer
Stay up-to-date with the latest COVID-19 statistics, with an interactive and informative user interface.

### Requirements
* Download MySQL Server at https://dev.mysql.com/downloads/mysql/
* Download MySQL Workbench at https://dev.mysql.com/downloads/workbench/
Make sure both are ready to go when moving to the next part.

### First Run
1. Open MySQL Workbench and create a new Schema called ```covid-19 global data displayer```.
2. Run [](connection.py) using ```py connection.py```. It might take a few minutes.
3. Run ```py server.py password``` to run the server, where ```password``` is the password for the MySQL account you created when installing the server. 
4. Access the application at ```http://localhost:8000```.

### Important Notes
* From now on, to use the application you should only run ```py server.py```.
* Before running the server, make sure the ```MySQL 8.0``` service is running on your machine.
To manually start the service:
  1. Search for 'Services' on Windows Search.
  2. Search for ```MySQL 8.0```.
  3. Manually start it.

### Contact
For further instrcutions and questions, please send us a mail at one of the following:
yairlevi2001@gmail.com
talsigman2001@gmail.com
