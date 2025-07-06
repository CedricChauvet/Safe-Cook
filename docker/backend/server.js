const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

// Connexion MySQL via pool
const pool = mysql.createPool({
  host: process.env.DB_HOST || '34.78.15.123',
  user: process.env.DB_USER || 'safecook',
  password: process.env.DB_PASSWORD || 'rootpassword',
  database: process.env.DB_NAME || 'safecook',
});

// Sign In
app.post('/auth/signin', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ message: 'Champs requis' });

  try {
    const [rows] = await pool.query(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );

    const user = rows[0];
    if (!user || user.password !== password) {
      return res.status(401).json({ message: 'Email ou mot de passe invalide' });
    }

    res.json({ message: 'Connexion réussie', userId: user.id });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Erreur serveur' });
  }
});

// Ping route (test)
app.get('/', (req, res) => res.send('API SafeCook OK'));
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Serveur démarré et écoute sur le port ${PORT}`);
});

app.get('/test-db', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT 1 + 1 AS solution');
    res.json({ solution: rows[0].solution });
  } catch (err) {
    console.error('Erreur test DB:', err);
    res.status(500).json({ error: 'Impossible de se connecter à la base' });
  }
});


app.post('/auth/signup', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password)
    return res.status(400).json({ message: 'Email et mot de passe requis.' });

  try {
    // Vérifier si l'utilisateur existe déjà
    const [existing] = await pool.query(
      'SELECT id FROM users WHERE email = ?',
      [email]
    );
    if (existing.length > 0) {
      return res.status(409).json({ message: 'Utilisateur déjà existant.' });
    }

    // Créer le nouvel utilisateur
    const [result] = await pool.query(
      'INSERT INTO users (email, password) VALUES (?, ?)',
      [email, password]
    );

    res.status(201).json({
      message: 'Utilisateur créé avec succès',
      userId: result.insertId,
    });
  } catch (err) {
    console.error('❌ Erreur signup:', err);
    res.status(500).json({ message: 'Erreur serveur lors de la création.' });
  }
});


app.post('/user/toggle-allergy', async (req, res) => {
  const { userId, allergyId } = req.body;

  if (!userId || !allergyId) {
    return res.status(400).json({ message: 'userId et allergyId requis.' });
  }

  try {
    // Vérifier si l'entrée existe déjà
    const [existing] = await pool.query(
      'SELECT * FROM user_allergies WHERE user_id = ? AND allergy_id = ?',
      [userId, allergyId]
    );

    if (existing.length > 0) {
      // Si existe, supprimer (toggle off)
      await pool.query(
        'DELETE FROM user_allergies WHERE user_id = ? AND allergy_id = ?',
        [userId, allergyId]
      );
      return res.status(200).json({ message: 'Allergie retirée.' });
    } else {
      // Sinon, insérer (toggle on)
      await pool.query(
        'INSERT INTO user_allergies (user_id, allergy_id) VALUES (?, ?)',
        [userId, allergyId]
      );
      return res.status(200).json({ message: 'Allergie ajoutée.' });
    }
  } catch (err) {
    console.error('❌ Erreur toggle allergy:', err);
    res.status(500).json({ message: 'Erreur serveur.' });
  }
});

app.get('/user/:userId/allergies', async (req, res) => {
  const { userId } = req.params;

  try {
    const [allergies] = await pool.query(
      `SELECT a.id, a.name
       FROM allergies a
       JOIN user_allergies ua ON a.id = ua.allergy_id
       WHERE ua.user_id = ?`,
      [userId]
    );

    // Optionnel: vous pouvez aussi retourner juste les IDs si vous préférez
    const allergyIds = allergies.map(allergy => allergy.id);

    res.status(200).json({ 
      allergies,        // Format actuel avec id et name
      allergyIds        // Format simplifié avec juste les IDs
    });
  } catch (err) {
    console.error('❌ Erreur récupération allergies:', err);
    res.status(500).json({ message: 'Erreur serveur.' });
  }
});