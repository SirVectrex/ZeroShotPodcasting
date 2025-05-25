
const { sql } = require('@vercel/postgres');

module.exports = async (req, res) => {

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed', message: 'This endpoint only supports GET requests.' });
  }

  try {

    const { rows } = await sql`SELECT COUNT(*) FROM ratings;`;

    const totalRatingsCount = parseInt(rows[0].count, 10);


    return res.status(200).json({ count: totalRatingsCount });

  } catch (error) {
    // Handle any errors during the database operation
    console.error('Error fetching total ratings count from database:', error);
    return res.status(500).json({ error: 'Failed to retrieve total ratings count', details: error.message });
  }
};