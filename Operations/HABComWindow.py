# Prototype window to be used for HAB team's communications platform

import sys
from PySide import QtGui

class CommWindow (QtGui.QMainWindow):

    def __init__(self):
        super (CommWindow, self).__init__()
        self.initUI()

    def initUI(self):               
        # Define menu bar actions
        exitAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        connectAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_connect.png'), 'Connect', self)
        connectAction.setStatusTip('Connect to Ballon')

        refreshAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_refresh.png'), 'Refresh', self)
        refreshAction.setStatusTip('Refresh All (Connection, Statistics, Location)') 
        
        locateAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_location.png'), 'Locate', self)
        locateAction.setStatusTip('Show Balloon Location')

        statsAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_stats.png'), 'Statistics', self)
        statsAction.setStatusTip('Show Flight Statistics')

        settingsAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_settings.png'), 'Settings', self)
        settingsAction.setStatusTip('Edit Settings')
        
        cutDownAction = QtGui.QAction(QtGui.QIcon('resHAB/glyphicons_fire.png'), 'Cut Down', self)
        cutDownAction.setStatusTip('Initiate Cut Down')
        
        # Add a menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        # Create the tool bar
        self.toolbar = self.addToolBar('ToolBarFav')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(connectAction)
        self.toolbar.addAction(refreshAction)
        self.toolbar.addAction(locateAction)
        self.toolbar.addAction(statsAction)
        self.toolbar.addAction(settingsAction)
        self.toolbar.addAction(cutDownAction)

        # Create the command line interface
        lblCommand = QtGui.QLabel('Command Line')
        boxCommand = QtGui.QTextEdit()
        lineCommand = QtGui.QLineEdit()

        # Create the grid layout and place all the widgets
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lblCommand, 1, 0)
        grid.addWidget(boxCommand, 2, 0)
        grid.addWidget(lineCommand, 3, 0)

        # A QMainWindow contains the central widget, which contains the layout grid
        centralWidget = QtGui.QWidget() 
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        
        # Show the status bar
        self.statusBar().showMessage('Ready')

        # Set window properties
        self.setGeometry(300, 300, 650, 500) # setGeometry(x,y,width,height)
        self.setWindowTitle('HAB Communications')
        self.setWindowIcon(QtGui.QIcon('resHAB/HABlogo.png'))
        self.show()



# Main Loop
app = QtGui.QApplication(sys.argv)
winMain = CommWindow()
sys.exit(app.exec_())
