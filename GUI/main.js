// Modules to control application life and create native browser window


const {
    app,
    BrowserWindow,
    ipcMain,
    Tray,
    Menu
} = require('electron');


global.vars = {
    firstGridUpdate: true,
    path: app.getPath("home")
};


function sendWindowMessage(targetWindow, message, payload) {
    if (typeof targetWindow === 'undefined') {
        console.log('Target window does not exist');
        return;
    }
    targetWindow.webContents.send(message, payload);
}


let mainWindow = null, workerWindow = null;


const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
    app.quit()
} else {
    app.on('second-instance', (event, commandLine, workingDirectory) => {
        // Someone tried to run a second instance, we should focus our window.
        if (mainWindow) {
            if (!mainWindow.isVisible()) mainWindow.show();
            else if (mainWindow.isMinimized()) mainWindow.restore()
            mainWindow.focus()
        }
    })

    // Create myWindow, load the rest of the app, etc...
    app.whenReady().then(() => {
        createWindow();

        //create link to worker:
        ipcMain.on('registerSim', (event, arg) => {
            console.log("passing data (main.js)");
            sendWindowMessage(workerWindow, 'registerSim', arg);
        });

        console.log("creating tray");

        let tray = new Tray('./icon.ico');

        const contextMenu = Menu.buildFromTemplate([
            {
                label: 'Show App', click: function () {
                    mainWindow.show();
                }
            },
            {
                label: 'Quit', click: function () {
                    mainWindow.destroy();
                    app.quit();
                }
            }
        ]);


        tray.setToolTip('EnvSim is running in the background');
        tray.setContextMenu(contextMenu)

        mainWindow.on('close', function (event) {
            event.preventDefault();
            mainWindow.hide();
        });


    })
}


function createWindow() {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        icon: "./icon.ico",
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true
        }
    });


    // create hidden worker window
    workerWindow = new BrowserWindow({
        show: false,
        webPreferences: {
            nodeIntegration: true,
            backgroundThrottling: false,
            enableRemoteModule: true
        }
    });
    workerWindow.loadFile('worker.html');

    mainWindow.maximize();

    require('electron-store');
    mainWindow.removeMenu()
    // and load the index.html of the app.
    mainWindow.loadFile('index.html')

    // Open the DevTools.
    mainWindow.webContents.openDevTools();
    // workerWindow.webContents.openDevTools();
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

