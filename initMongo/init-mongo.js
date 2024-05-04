var db = db.getSiblingDB('ppna_db');
db.createCollection('users');
db.createCollection('ppna');

// Function to insert data from CSV file into a collection
function insertDataFromCSV(collectionName, csvFilePath) {
    // Read the CSV file
    var csvData = cat(csvFilePath);

    // Split CSV data by lines
    var lines = csvData.split('\n');

    // Assuming the first line contains headers
    var headers = lines[0].split(',');

    // Iterate over each line (excluding header)
    for (var i = 1; i < lines.length; i++) {
        var line = lines[i].trim();
        if (line) { // Skip empty lines
            var fields = line.split(',');
            var document = {};
            // Map CSV data to MongoDB document fields based on headers
            for (var j = 0; j < headers.length; j++) {
                document[headers[j].trim()] = fields[j].trim();
            }
            // Insert document into the collection
            db.getCollection(collectionName).insert(document);
        }
    }
}

// Insert data from CSV file into 'ppna' collection
insertDataFromCSV('ppna', './ppna.csv');
