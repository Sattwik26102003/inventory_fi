

const fs = require('fs');
const path = require('path');
const db = require('./db'); 

const init = async () => {
  try {
    const schemaPath = path.join(__dirname, 'schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf-8');
    console.log('Running database schema setup...');
    await db.query(schema);
    console.log('Database schema setup complete.');
  } catch (error) {
    console.error('Failed to setup database schema:', error);
  } 
};

init();
