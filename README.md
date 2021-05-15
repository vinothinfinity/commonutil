# commonutil

----------------------------------
START -> Find Vaccination slot UTIL
----------------------------------

Usage:
------
python3 vaccine.py

Quick look inside:
------------------
1) Copy vaccine.py into a folder and also create an empty log file “vaccine.log” in same folder and give absolute path of log inside the vaccine.py
2) debug = False <<  True prints output in screen, False redirect to file. I suggest using True and check whether script works.
3) I have added a beep code so whenever slot is found, it actually does beep 10 times.
4) In mail you can repeat same steps for one more district code. (steps to find district code is in file top)
 
Cron job:
---------
Steps
1) crontab -e
opens a editor
2) enter below line
* * * * * /usr/bin/python3 /Users/vratnaku/Downloads/new_exports/vacMe/vaccine.py >> /tmp/cron.out
3) save and quit
:wq  (save and quit the editor)
4) tail for output
tail -f /tmp/cron.out
 
Output:
-------
2021-05-12 18:52:07,609 - INFO - ('14/05/2021  Total Slots Available[Age:18]: ', '203')
2021-05-12 18:52:07,610 - INFO -
1  . Hospital Name: MGM COVAXIN                             , Availability:1   , Vaccine:COVAXIN            
2  . Hospital Name: MGM COVAXIN                             , Availability:202 , Vaccine:COVAXIN            
 
2021-05-12 18:52:07,610 - INFO - ****
2021-05-12 18:52:10,504 - INFO - ****
2021-05-12 18:52:10,504 - INFO - ('15/05/2021  Total Slots Available[Age:18]: ', '181')
2021-05-12 18:52:10,504 - INFO -
1  . Hospital Name: MGM COVAXIN                             , Availability:1   , Vaccine:COVAXIN            
2  . Hospital Name: MGM COVAXIN                             , Availability:180 , Vaccine:COVAXIN            
 
2021-05-12 18:52:10,504 - INFO - ****
  
Remember to login and book once u find slots via scripts. Cron job will give beep sound 😊

----------------------------------
END -> Find Vaccination slot UTIL
----------------------------------
