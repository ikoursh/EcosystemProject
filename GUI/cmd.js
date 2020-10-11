//Uses node.js process manager
const electron = require('electron');
const child_process = require('child_process');
const dialog = electron.dialog;

// This function will output the lines from the script
// and will return the full combined output
// as well as exit code when it's done (using the callback).
exports.run_script = function(command, args, callback, dataCallback) {
  var child = child_process.spawn(command, args, {
    encoding: 'utf8',
    shell: true
  });

  child.stdout.setEncoding('utf8');
  child.stdout.on('data', (data) => {
    //Here is the output
    // data=data.toString();

    var lines = data.match(/[^\r\n]+/g);
    for (var i = 0; i < lines.length; i++) {
      console.log(lines[i]);

      dataCallback([lines[i], 0]);
    }
  });

  child.stderr.setEncoding('utf8');
  child.stderr.on('data', (data) => {
    // Return some data to the renderer process with the mainprocess-response ID
    // mainWindow.webContents.send('mainprocess-response', data);
    // data=data.toString();
    var lines = data.match(/[^\r\n]+/g);
    for (var i = 0; i < lines.length; i++) {
      console.log(lines[i]);
      
      dataCallback([lines[i], -1]);
    }
    // dataCallback([data, -1]);
  });

  if (typeof callback === 'function')
    callback();
};
