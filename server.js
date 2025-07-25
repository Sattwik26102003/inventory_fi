
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use('/api/auth', authRoutes);
app.use('/api', productRoutes);

app.get('/', (req, res) => {
  res.send('Welcome to the Inventory Management API with PostgreSQL!');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
