from graphics import *

import serial
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]

arduinoInfo = ['hour','min','sec','day','soil','temp','humidity']
textInfos = [Text(Point(70,85), 'NA'),Text(Point(210,85), 'NA'), Text(Point(350,85),'NA'), Text(Point(70, 185),'NA'), Text(Point(210,185),'Sun 11:59PM')]

win = GraphWin('WaterWorks', 420, 500)

pumpStatus = False
pumpStatusTextValue = Text(Point(210, 385), 'OFF')
pumpStatusTextValue.setTextColor('black')
pumpStatusTextValue.draw(win)

def printPumpStatus():
    if(pumpStatus):
        pumpStatusTextValue.setTextColor('red')
        pumpStatusTextValue.setText('ON')
    else:
        pumpStatusTextValue.setTextColor('black')
        pumpStatusTextValue.setText('OFF')

def inside(point, rectangle):
    """ Is point inside rectangle? """

    ul = rectangle.getP1()  #p1 is ul (upper left)
    lr = rectangle.getP2()  #p2 is lr (lower right)

    return ul.getX() < point.getX() < lr.getX() and ul.getY() < point.getY() < lr.getY()

def getInfo():
    global arduinoInfo
    if(str(ser.readline())[2:7] == "start"):
        hour = str(ser.readline())
        arduinoInfo[0] = hour[2:4]
        arduinoInfo[1] = (str(ser.readline()))[2:4]
        arduinoInfo[2] = (str(ser.readline()))[2:4]
        arduinoInfo[3] = (str(ser.readline()))[2:5]
        arduinoInfo[4] = (str(ser.readline()))[2:5]
        arduinoInfo[5] = (str(ser.readline()))[2:4]
        arduinoInfo[6] = (str(ser.readline()))[2:4]

def initTextAreas():
    global textInfos
    for t in textInfos:
        t.draw(win)
        
def updateValues():
    global textInfos
    textInfos[0].setText(arduinoInfo[0] + ':' + arduinoInfo[1] + ':' + arduinoInfo[2])
    textInfos[1].setText(arduinoInfo[5] + "F")
    textInfos[3].setText(arduinoInfo[4] + " units")
def main():
    global pumpStatus
    global arduinoInfo
    win.setBackground('grey')
    message = Text(Point(win.getWidth()/2, 20), 'Taking care of Croton')
    message.setTextColor('yellow')
    message.setStyle('bold')
    message.setSize(10)
    message.draw(win)
    
    timeBox = Rectangle(Point(20,50), Point(120,100))
    timeBox.draw(win)
    timeText = Text(Point(70,60),'Current Time: ')
    timeText.setTextColor('white')
    timeText.setStyle('bold')
    timeText.setSize(8)
    timeText.draw(win)
    
    tempBox = Rectangle(Point(160,50), Point(260,100))
    tempBox.draw(win)
    tempText = Text(Point(210,60),'Current Temp: ')
    tempText.setTextColor('white')
    tempText.setStyle('bold')
    tempText.setSize(8)
    tempText.draw(win)
    
    pressureBox = Rectangle(Point(300, 50), Point(400,100))
    pressureBox.draw(win)
    pressureText = Text(Point(350, 60),'Current Pressure: ')
    pressureText.setTextColor('white')
    pressureText.setStyle('bold')
    pressureText.setSize(7)
    pressureText.draw(win)
    
    moistureBox = Rectangle(Point(20,150), Point(120, 200))
    moistureBox.draw(win)
    moistureText = Text(Point(70, 160), 'Current Humidity: ')
    moistureText.setTextColor('white')
    moistureText.setStyle('bold')
    moistureText.setSize(7)
    moistureText.draw(win)
    
    lastWateredBox = Rectangle(Point(160,150), Point(260, 200))
    lastWateredBox.draw(win)
    lastWateredText = Text(Point(210, 160), 'Last Watered: ')
    lastWateredText.setTextColor('white')
    lastWateredText.setStyle('bold')
    lastWateredText.setSize(8)
    lastWateredText.draw(win)
    
    sunlightBox = Rectangle(Point(300, 150), Point(400, 200))
    sunlightBox.draw(win)
    sunlightText = Text(Point(350, 160), 'Sunlight today: ')
    sunlightText.setTextColor('white')
    sunlightText.setStyle('bold')
    sunlightText.setSize(7)
    sunlightText.draw(win)
    
    pumpOnButton = Rectangle(Point(20, 350), Point(120, 400))
    pumpOnButton.draw(win)
    pumpOnText = Text(Point(70, 375), 'Turn Pump ON')
    pumpOnText.setTextColor('white')
    pumpOnText.setStyle('bold')
    pumpOnText.setSize(7)
    pumpOnText.draw(win)
    
    pumpOffButton = Rectangle(Point(300, 350), Point(400, 400))
    pumpOffButton.draw(win)
    pumpOffText = Text(Point(350, 375), 'Turn Pump OFF')
    pumpOffText.setTextColor('white')
    pumpOffText.setStyle('bold')
    pumpOffText.setSize(7)
    pumpOffText.draw(win)
    
    pumpStatusText = Text(Point(210, 360), 'Pump is:')
    pumpStatusText.setTextColor('white')
    pumpStatusText.draw(win)
    
    initTextAreas()
    while(True):
        getInfo()
        print(arduinoInfo)
        updateValues()
        clickPoint = win.checkMouse()
        if clickPoint is None:
            continue
        elif(inside(clickPoint, pumpOnButton)):
            pumpStatus = True
            printPumpStatus()
            #Turn the pump on
        elif(inside(clickPoint, pumpOffButton)):
            pumpStatus = False
            printPumpStatus()
            #turn pump off
            
main()

