# stockgraphics
sorts of stock daily charts , real time curve graph etc , make and show the usage of pyqtgraph 


![stock real time quadrants pix](/pix/quadrantspix.png)
## TASKS

### Display the bidding volume distribution along the Horizontal X axis 
1. Draw Horizontal Line from the Vertical Y axis , representing the volume of 
    each price bidding.
## TODO:
    - break the monolith app into pieces of microservices -
    - set grabbing real time datum as a standalone service
        * config designating the stock list 
    - another service provide datum ETL / transformation
    - the pyqtgraphics providing view  to the user -
    1. employing peewee as orm

## Daily Time Spending Recorder
    1. Jobs done ==> created a Class representing the Graphic Items 
    2. Vertically Drawing Volumes of the spreading bidding prices . spectrum 
    3. the solo goal to fulfill the dramatic drawing line graph of the stock real time 
    plotting , receiving data from hq.sina.com
    1. pack the lines of data to a data frame of pandas
    1. stack all of the each of bidding price, corresponding volume to the Vertical 
    1. Test graph items setting layout.
    1. the order of the developing is in  such a sequence as below described:
        *  deteriment the layout , used the examples code
        *  capsulating the datum , price line data then volume data 
        *  Display in one same plotting eara .
    1.  sh index to candle sticks --not implemented yet TODO

### modify the example codes of pyqtgraphic , candlesticks.py 
### Learn to implementing the various features of pyqtgraphic tools  
