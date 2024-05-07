db = db.getSiblingDB('ppna_db');

db.createCollection('user');
db.createCollection('ppna');

// Importar el módulo 'fs' para leer el archivo CSV
const fs = require('fs');

// Leer el contenido del archivo CSV
const csvData = fs.readFileSync('/docker-entrypoint-initdb.d/ppna.csv', 'utf8');

// Convertir los datos CSV en un array de objetos
const rows = csvData.trim().split('\n');
const keys = rows.shift().split(',');
const jsonData = rows.map(row => {
    const values = row.split(',');
    return keys.reduce((obj, key, index) => {
        obj[key] = values[index];
        return obj;
    }, {});
});


// Insertar los datos en la colección
const collection = db.getCollection('ppna');
collection.insertMany(jsonData);