// botvar.js

const fs = require('fs');
const express = require('express');
const { Client, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const path = './conversaciones.csv';
const mediaFolder = './media';

// Crear la carpeta 'media' si no existe
if (!fs.existsSync(mediaFolder)){
    fs.mkdirSync(mediaFolder);
}

const app = express();
app.use(express.json());  // Middleware para aceptar JSON

const client = new Client();
let mensajes = [];  // Lista temporal de mensajes

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneá este código QR para conectarte a WhatsApp');
});

client.on('ready', () => {
    console.log('WhatsApp Web está conectado.');
});

// Función para guardar mensajes en CSV con codificación UTF-8
const guardarMensajeCSV = (numero, mensaje, esBot, esMedia = false, rutaMedia = '') => {
    const header = "Numero,Mensaje,Fecha,EnviadoPorBot,EsMedia,RutaMedia\n";
    const nuevaLinea = `${numero},"${mensaje.replace(/"/g, '""').replace(/\n/g, " ")}",${new Date().toLocaleString()},${esBot},${esMedia},${rutaMedia}\n`;

    if (!fs.existsSync(path)) {
        fs.writeFileSync(path, header, { encoding: 'utf-8' });
    }

    fs.appendFileSync(path, nuevaLinea, { encoding: 'utf-8' });
};

// Guardar mensajes en la lista temporal y en el CSV
client.on('message_create', async (message) => {
    const esBot = message.fromMe ? true : false;
    
    if (message.hasMedia) {
        const media = await message.downloadMedia();
        const extension = media.mimetype.split('/')[1];
        const rutaArchivo = `${mediaFolder}/${message.id.id}.${extension}`;
        fs.writeFileSync(rutaArchivo, media.data, { encoding: 'base64' });

        guardarMensajeCSV(message.from, "Media file", esBot, true, rutaArchivo);
        mensajes.push({ numero: message.from, mensaje: "Media file", esBot, esMedia: true, rutaMedia: rutaArchivo });
    } else {
        guardarMensajeCSV(message.from, message.body, esBot);
        mensajes.push({ numero: message.from, mensaje: message.body, esBot, esMedia: false });
    }

    console.log(`Mensaje guardado de ${message.from}: ${message.body} (Enviado por bot: ${esBot})`);
});

// Ruta para obtener los mensajes en Streamlit
app.get('/mensajes', (req, res) => {
    res.json(mensajes);
});

// Ruta para enviar un mensaje
app.post('/enviar-mensaje', (req, res) => {
    const { numero, mensaje } = req.body;
    client.sendMessage(numero, mensaje)
        .then(response => {
            guardarMensajeCSV(numero, mensaje, true);
            mensajes.push({ numero: numero, mensaje: mensaje, esBot: true, esMedia: false, rutaMedia: '' });
            res.status(200).json({ success: true, message: 'Mensaje enviado' });
        })
        .catch(err => res.status(500).json({ success: false, error: err }));
});

client.initialize();

app.listen(3000, () => {
    console.log('Servidor API escuchando en http://localhost:3000');
});
