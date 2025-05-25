
const { sql } = require('@vercel/postgres');


const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed', message: 'This endpoint only supports GET requests.' });
  }

  try {
    console.log('Fetching all ratings from database...');
    // Fetch all necessary columns: file, rating, and is_human
    const { rows: ratings } = await sql`SELECT file, rating, is_human FROM ratings;`;
    console.log(`Fetched ${ratings.length} ratings.`);

    const metadataPath = path.join(__dirname, '..', 'data', 'audio_metadata.json');
    console.log(`Reading metadata from: ${metadataPath}`);

    let metadata;
    try {
        // Read the metadata file content
        const metadataContent = fs.readFileSync(metadataPath, 'utf8');
        // Parse the JSON content
        metadata = JSON.parse(metadataContent);
        console.log(`Successfully read metadata for ${Object.keys(metadata).length} files.`);
    } catch (readError) {
        console.error('Error reading metadata file:', readError);
        // If metadata is critical for this function, return an error
        return res.status(500).json({ error: 'Failed to read audio metadata', details: readError.message });
    }

    const modelStats = {};

    ratings.forEach(ratingEntry => {
      const { file, rating, is_human } = ratingEntry; 

      const info = metadata[file];

      if (!info || info.style !== 'conversational') {
        return; // Move to the next rating entry
      }

      const { model, label } = info; // label is the 'correct' answer from metadata

      if (!modelStats[model]) {
        modelStats[model] = { ratings: [], correct: 0, total: 0 };
      }

      modelStats[model].ratings.push(Number(rating));

      const isRatingHuman = is_human === true; // Convert boolean from DB to a concept of 'human' rating
      const isLabelHuman = label === 'human'; // Convert label string to a concept of 'human' label

      if (isLabelHuman === isRatingHuman) { // Check if the boolean values match
          modelStats[model].correct++;
      }
      
      modelStats[model].total++;
    });

    console.log(`Aggregated stats for ${Object.keys(modelStats).length} conversational models.`);

    const leaderboard = Object.entries(modelStats).map(([model, stats]) => {
      const avgRating = stats.ratings.length > 0
        ? (stats.ratings.reduce((a, b) => a + b, 0) / stats.ratings.length)
        : 0; // Default to 0 if no ratings

      const correctness = stats.total > 0
        ? (stats.correct / stats.total) * 100
        : 0; // Default to 0 if no total votes

      // Return the formatted object for each model
      return {
        model,
        avgRating: avgRating.toFixed(2), // Format average rating to 2 decimal places
        correctness: correctness.toFixed(1) + '%', // Format correctness to 1 decimal place and add '%' sign
        totalVotes: stats.total // Include the total number of votes
      };
    });

    leaderboard.sort((a, b) => parseFloat(b.correctness) - parseFloat(a.correctness));


    console.log('Returning conversational leaderboard data.');
    res.status(200).json(leaderboard);

  } catch (error) {
    console.error('Caught error generating conversational leaderboard:', error);
    // Return a 500 Internal Server Error response with details
    res.status(500).json({ error: 'Error fetching conversational leaderboard data', details: error.message });
  }
};
