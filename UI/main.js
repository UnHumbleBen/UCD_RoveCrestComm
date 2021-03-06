// Modules to control application life and create native browser window
const { app, BrowserWindow, webContents } = require('electron')
const jimp = require('jimp');
const net = require('net');
const path = require('path');
const cv = require('./opencv.js');


// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

// Sockets
const SCK_MSG_PORT = 9999
const SCK_VID_PORT = 1234
let sckVidClient
let sckMsgClient

// Video variables
const FRAME_SIZE_NOT_READY = -1         // Used for `frameSize` variable to indicate
                                        // that frameSize is not known yet.
const FRAME_PAYLOAD_SIZE = 4            // Frame size is specified in 4 bits.
let frameSize = FRAME_SIZE_NOT_READY;   // Global variable that tracks frameSize, -1 if not ready.
let videoDataBuffer = Buffer.alloc(0);  // Global variable that tracks frame data.


function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    // fullscreen: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true
    },
    show: false,  // Delay show to attach listener for event 'ready-to-show'
  })

  // When the web page has been rendered, attach camera feed to window.
  mainWindow.on('ready-to-show', () => {
    mainWindow.show();
    attachCameraFeed(mainWindow.webContents)
  });
  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    app.quit();
    sckMsgClient.destroy();
    sckVidClient.destroy();
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

/**
 * Set up sockets needed for
 * @param {WebContents} webContents Main window web contents.
 */
function attachCameraFeed(webContents) {
  // Connect video socket
  sckVidClient = new net.Socket();
  sckVidClient.connect(SCK_VID_PORT, '127.0.0.1',function() {
    console.log("Connected to video socket");
  });

  sckVidClient.on('data', function(data) {
    // Accumalate video data buffer.
    videoDataBuffer = Buffer.concat([videoDataBuffer, data]);
    // Process video data, sending video to main window if needed.
    processVidData(videoDataBuffer, webContents);
  });

  sckVidClient.on('close', function() {
    console.log('Video connection closed');
  });

  // Connect messenger socket
  sckMsgClient = new net.Socket();
  sckMsgClient.connect(SCK_MSG_PORT, '127.0.0.1', function() {
    console.log("Connected to message socket");
  });

  sckMsgClient.on('data', function(data) {
  });

  sckMsgClient.on('close', function() {
    console.log('Message connection closed');
  });
}

/**
 * Process the fully accumulated data buffer, including reading frame size,
 * reading frame data, and sending frame data to main window.
 *
 * @param {Buffer} data The accumulated data buffer.
 * @param {WebContents} contents The event emitter for the window to send to.
 */
async function processVidData(data, contents) {
  // If frame size has not been set yet, try to fetch it from buffer
  if (frameSize == FRAME_SIZE_NOT_READY) {
    try {
      frameSize = videoDataBuffer.readInt32LE();
      videoDataBuffer = videoDataBuffer.slice(FRAME_PAYLOAD_SIZE);
    } catch { }
  }

  // If frame size is ready and frame data buffer is ready, then read frame
  if (frameSize != FRAME_SIZE_NOT_READY && videoDataBuffer.length >= frameSize) {
    // Retrieve frame data.
    const frameData = videoDataBuffer.slice(0, frameSize);

    // Send data to frontend.
    contents.send('rover', frameData.toString());

    // Remove frame data from accumulated data buffer.
    videoDataBuffer = videoDataBuffer.slice(frameSize);
    // Reset frame size.
    frameSize = FRAME_SIZE_NOT_READY;
  }
}
