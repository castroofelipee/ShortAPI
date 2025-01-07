const { app, BrowserWindow, ipcMain } = require('electron');
const axios = require('axios'); 
const path = require('path');

let win;

function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
        },
    });

    win.loadFile('interface/index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

ipcMain.handle("download-video", async (event, url, format) => {
    try {
        const response = await axios.post('http://localhost:8000/downloads/', {
            url: url,
            format: format
        });

        return { file: response.data.file };
    } catch (error) {
        console.error("Erro ao comunicar com o backend", error);
        return { error: "Erro ao comunicar com o servidor!" };
    }
});
