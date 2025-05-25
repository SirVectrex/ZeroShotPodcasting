const { sql } = require('@vercel/postgres');

module.exports = async (req, res) => {

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { file, rating, isHuman, type } = req.body;

  // Ensure all required fields are present (even if they are empty strings or null/undefined)
  if (file === undefined || file === null || file === '' ||
      rating === undefined || rating === null || // Rating might be 0, so don't check for emptiness
      isHuman === undefined || isHuman === null ||
      type === undefined || type === null || type === ''
     )
  {
       return res.status(400).json({ error: 'Missing required fields' });
  }


  const parsedRating = parseInt(rating, 10);

  const parsedIsHuman = (isHuman !== 'robot'); // This will be true if isHuman is 'human', false if 'robot'

   if (
      typeof file !== 'string' ||
      typeof type !== 'string' ||
      isNaN(parsedRating) // Check if the parseInt conversion resulted in Not-a-Number
     )
  {
       return res.status(400).json({ error: 'Invalid data types received' });
  }


  try {
    await sql`
      INSERT INTO ratings (file, rating, is_human, type)
      VALUES (${file}, ${parsedRating}, ${parsedIsHuman}, ${type});
    `;

    return res.status(200).json({ message: 'Rating submitted. Loading next...' });
  } catch (error) {
    // Handle any errors during the database operation (e.g., DB connection issues)
    console.error('Error saving rating to Neon database:', error);
    return res.status(500).json({ error: 'Failed to save rating to database', details: error.message });
  }
};