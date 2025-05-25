const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  let type = req.query.type; // Get the type from the query string
  const ratedFilesJson = req.query.rated; // Get the list of rated files as a JSON string

  let ratedFiles = [];
  if (ratedFilesJson) {
    try {
      ratedFiles = JSON.parse(ratedFilesJson);
      // Ensure it's actually an array
      if (!Array.isArray(ratedFiles)) {
          ratedFiles = [];
          console.warn('Received invalid rated files data (not an array):', ratedFilesJson);
      }
    } catch (e) {
      console.error('Failed to parse rated files JSON:', ratedFilesJson, e);
      ratedFiles = []; // Default to empty if parsing fails
    }
  }

  // List of types to check, starting with either the requested type or a random one
  const typesToCheck = [];
  if (type && (type === 'monologue' || type === 'conversational')) {
      typesToCheck.push(type);
      // Add the other type as a fallback
      typesToCheck.push(type === 'monologue' ? 'conversational' : 'monologue');
  } else {
      // If no valid type is requested, randomly choose a starting type and add the other
      const randomType = Math.random() < 0.5 ? 'monologue' : 'conversational';
      typesToCheck.push(randomType);
      typesToCheck.push(randomType === 'monologue' ? 'conversational' : 'monologue');
  }


  let foundFile = null;
  let chosenType = null;

  // Iterate through the types (starting with the preferred/random one)
  for (const currentType of typesToCheck) {
      const folderPath = path.join(__dirname, `../public/audio/${currentType}`);

      // Ensure the folder exists
      if (!fs.existsSync(folderPath)) {
        console.warn(`Audio folder not found for type '${currentType}': ${folderPath}`);
        continue; // Skip this type if folder is missing
      }

      const files = fs.readdirSync(folderPath)
                        .filter(file => file.endsWith('.wav'))
                        .map(file => `${currentType}/${file}`); // Create full identifier (e.g., 'monologue/audio1.wav')

      // Filter out files the user has already rated
      const unratedFiles = files.filter(file => !ratedFiles.includes(file));

      if (unratedFiles.length > 0) {
          // Found unrated files, pick one randomly
          const chosenIdentifier = unratedFiles[Math.floor(Math.random() * unratedFiles.length)];
          foundFile = chosenIdentifier.split('/')[1]; // Extract just the filename
          chosenType = currentType; // Store the type it came from
          break; // Found a file, exit the loop
      }
  }

  if (foundFile && chosenType) {
    // Return both the filename (including the type folder) and the type
    return res.json({ filename: `${chosenType}/${foundFile}`, type: chosenType });
  } else {
    // No unrated files found in either category
    return res.status(404).json({ error: 'No unrated audio files available.' });
  }
};