

const jwt = require('jsonwebtoken');
const { JWT_SECRET } = process.env; 

module.exports = function(req, res, next) {
  const authHeader = req.header('Authorization');

  if (!authHeader) {
    return res.status(401).json({ msg: 'No token, authorization denied' });
  }

  const tokenParts = authHeader.split(' ');
  if (tokenParts.length !== 2 || tokenParts[0] !== 'Bearer') {
    return res.status(401).json({ msg: 'Token format is not "Bearer <token>"' });
  }
  
  const token = tokenParts[1];

  try {
    const decoded = jwt.verify(token, JWT_SECRET);

    req.user = decoded.user;
    
    next();
  } catch (err) {
    res.status(401).json({ msg: 'Token is not valid' });
  }
};
