const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    downloadVideo: (url, format) => ipcRenderer.invoke('download-video', url, format)
});
