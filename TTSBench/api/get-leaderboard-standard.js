
const { sql } = require('@vercel/postgres');

const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed', message: 'This endpoint only supports GET requests.' });
  }

  try {
    console.log('Fetching all ratings from database...');
    const { rows: ratings } = await sql`SELECT file, rating, is_human FROM ratings;`;
    console.log(`Fetched ${ratings.length} ratings.`);

    const metadataPath = path.join(__dirname, '..', 'data', 'audio_metadata.json');
    console.log(`Reading metadata from: ${metadataPath}`);

    let metadata;
    try {
        const metadataContent = fs.readFileSync(metadataPath, 'utf8');
        metadata = JSON.parse(metadataContent);
        console.log(`Successfully read metadata for ${Object.keys(metadata).length} files.`);
    } catch (readError) {
        console.error('Error reading metadata file:', readError);
        return res.status(500).json({ error: 'Failed to read audio metadata', details: readError.message });
    }


    const modelStats = {};

    ratings.forEach(ratingEntry => {
      const { file, rating, is_human } = ratingEntry; 
      const info = metadata[file];

      if (!info || info.style !== 'standard') {
        return;
      }

      const { model, label } = info; // label is the 'correct' answer from metadata

      if (!modelStats[model]) {
        modelStats[model] = { ratings: [], correct: 0, total: 0 };
      }

      modelStats[model].ratings.push(Number(rating)); // Convert DB value to Number

      const isRatingHuman = is_human === true;
      const isLabelHuman = label === 'human';

      if (isLabelHuman === isRatingHuman) { // Check if the boolean values match
          modelStats[model].correct++;
      }
      modelStats[model].total++;
    });

    console.log(`Aggregated stats for ${Object.keys(modelStats).length} models.`);

    const leaderboard = Object.entries(modelStats).map(([model, stats]) => {
      const avgRating = stats.ratings.length > 0
        ? (stats.ratings.reduce((a, b) => a + b, 0) / stats.ratings.length)
        : 0; // Handle case with no ratings to avoid division by zero

      const correctness = stats.total > 0
        ? (stats.correct / stats.total) * 100
        : 0; // Handle case with no total votes

      return {
        model,
        avgRating: avgRating.toFixed(2), // Format to 2 decimal places
        correctness: correctness.toFixed(1) + '%', // Format to 1 decimal place and add '%'
        totalVotes: stats.total
      };
    });

    leaderboard.sort((a, b) => parseFloat(b.correctness) - parseFloat(a.correctness));


    console.log('Returning leaderboard data.');
    res.status(200).json(leaderboard);

  } catch (error) {
    console.error('Caught error generating leaderboard:', error);
    res.status(500).json({ error: 'Error fetching leaderboard data', details: error.message });
  }
};
