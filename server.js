const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON or URL encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files (CSS, JS, Images)
app.use(express.static(path.join(__dirname)));

// Route for signup page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'signup.html'));
});

// You can handle POST request from signup here (optional)
app.post('/signup', (req, res) => {
  const { name, email, password } = req.body;
  console.log('Signup Data:', name, email, password);

  // You can store to DB here or return a response
  res.status(200).json({ message: 'Signup successful!' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`✅ Server is running at: http://localhost:${PORT}`);
});
