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
        key_trimmed=key.trim();
        value_trimmed=values[index].trim();
        obj[key_trimmed] = value_trimmed;
        return obj;
    }, {});
});

const collection = db.getCollection('ppna');
collection.insertMany(jsonData);

// Actualizar los documentos en la colección utilizando $project
collection.aggregate([
  {
    $addFields: {
      location: {
        type: "Point",
        coordinates: [
          { $toDouble: "$longitude" },
          { $toDouble: "$latitude" }
        ]
      }
    }
  },
  {
    $project: {
      _id: 1,
      location: 1
    }
  }
]).forEach(document => {
  collection.updateOne(
    { _id: document._id }, // Filtro para encontrar el documento
    { $set: { location: document.location } } // Actualización del campo location
  );
});