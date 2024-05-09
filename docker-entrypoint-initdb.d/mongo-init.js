// Conecta a la base de datos 'ppna_db'
db = db.getSiblingDB('ppna_db');

// Crea las colecciones
db.createCollection('user');
db.createCollection('ppna');

// Importar el módulo 'fs' para leer el archivo CSV
import { readFileSync } from 'fs';

// Leer el contenido del archivo CSV
const csvData = readFileSync('/docker-entrypoint-initdb.d/ppna.csv', 'utf8');

// Convertir los datos CSV en un array de objetos GEOJson
const rows = csvData.trim().split('\n');
const keys = rows.shift().split(',');
const jsonData = rows.map(row => {
    const values = row.split(',');
    const data = keys.reduce((obj, key, index) => {
        obj[key] = values[index];
        return obj;
    }, {});

    // Convertir latitud y longitud en objetos GEOJson
    if (data['latitude'] && data['longitude']) {
        data['location'] = {
            'type': 'Point',
            'coordinates': [
                parseFloat(data['longitude']),
                parseFloat(data['latitude']),
            ],
        };
    }

    return data;
});

// Insertar los datos en la colección 'ppna'
const collection = db.getCollection('ppna');
collection.insertMany(jsonData);

// Crear un índice geoespacial 2dsphere para la colección 'ppna'
collection.createIndex({ 'location': '2dsphere' });

// Imprimir algunos puntos para verificar la inserción
const points = collection.find().limit(10).toArray();
print('Primeros puntos insertados:', points);





// db = db.getSiblingDB('ppna_db');

// db.createCollection('user');
// db.createCollection('ppna');

// // Importar el módulo 'fs' para leer el archivo CSV
// const fs = require('fs');

// // Leer el contenido del archivo CSV
// const csvData = fs.readFileSync('/docker-entrypoint-initdb.d/ppna.csv', 'utf8');

// // Convertir los datos CSV en un array de objetos
// const rows = csvData.trim().split('\n');
// const keys = rows.shift().split(',');
// const jsonData = rows.map(row => {
//     const values = row.split(',');
//     return keys.reduce((obj, key, index) => {
//         obj[key] = values[index];
//         return obj;
//     }, {});
// });


// // Insertar los datos en la colección
// const collection = db.getCollection('ppna');
// collection.insertMany(jsonData);