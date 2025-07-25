
require('dotenv').config();
const { Pool } = require('pg');

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT || 5432,
});

pool.connect((err, client, release) => {
  if (err) {
    return console.error('Error acquiring client', err.stack);
  }
  console.log('PostgreSQL database connected successfully.');
  client.release();
});


module.exports = {
  /**
   * Executes a SQL query against the database.
   * @param {string} text - The SQL query string.
   * @param {Array} params - The parameters to pass to the query.
   * @returns {Promise<QueryResult>} The result of the query.
   */
  query: (text, params) => pool.query(text, params),
};
