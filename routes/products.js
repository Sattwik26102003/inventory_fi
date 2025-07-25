

const express = require('express');
const authMiddleware = require('../middleware/authMiddleware');
const db = require('../db/db'); 

const router = express.Router();

router.post('/products', authMiddleware, async (req, res) => {
  const { name, type, sku, image_url, description, quantity, price } = req.body;

  try {
    const insertQuery = `
      INSERT INTO products (name, type, sku, image_url, description, quantity, price)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING id;
    `;
    const values = [name, type, sku, image_url, description, quantity, price];
    const result = await db.query(insertQuery, values);
    
    res.status(201).json({ product_id: result.rows[0].id, msg: 'Product added successfully' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

router.get('/products', authMiddleware, async (req, res) => {
  const page = parseInt(req.query.page, 10) || 1;
  const limit = parseInt(req.query.limit, 10) || 10;
  const offset = (page - 1) * limit;

  try {
    const productsQuery = 'SELECT * FROM products ORDER BY created_at DESC LIMIT $1 OFFSET $2';
    const { rows } = await db.query(productsQuery, [limit, offset]);
    res.json(rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

router.put('/products/:id/quantity', authMiddleware, async (req, res) => {
  const { quantity } = req.body;
  const { id } = req.params;

  if (typeof quantity !== 'number') {
    return res.status(400).json({ msg: 'Quantity must be a number.' });
  }

  try {
    const updateQuery = 'UPDATE products SET quantity = $1 WHERE id = $2 RETURNING *';
    const { rows } = await db.query(updateQuery, [quantity, id]);

    if (rows.length === 0) {
      return res.status(404).json({ msg: 'Product not found' });
    }

    res.json(rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
