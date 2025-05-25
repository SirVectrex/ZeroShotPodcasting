const express = require('express');
const path = require('path');
const fs = require('fs');
const router = express.Router();

// Utility function to get audio files from a specific directory
const getAudioFiles = (type) => {
  const audioDir = path.join(__dirname, 'audio', type); // Adjust 'audio' path as per your directory structure
  const files = fs.readdirSync(audioDir);

  return files.map(file => {
    return {
      filename: file,
      model: file.split('-')[0],  // Assuming the filename structure is like "modelname-audiofile.wav"
      type: type
    };
  });
};

// Endpoint to get all monologue audio files
router.get('/api/get-audio-files', (req, res) => {
  const { type } = req.query;

  if (!type || (type !== 'monologue' && type !== 'conversational')) {
    return res.status(400).json({ error: 'Invalid type, must be "monologue" or "conversational".' });
  }

  try {
    const audioFiles = getAudioFiles(type);
    res.json(audioFiles);
  } catch (error) {
    console.error('Error fetching audio files:', error);
    res.status(500).json({ error: 'Error fetching audio files. Please try again later.' });
  }
});

module.exports = router;
