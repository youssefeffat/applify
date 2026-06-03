/**
 * Calculates a match score between a job and a user profile
 * @param {import('../api/jobs').Job} job - The job posting object
 * @param {Object} user - The user profile object
 * @returns {{score: number, fitsPreferences: boolean, isRecommended: boolean, shouldDisplay: boolean}} The match result
 */
export function calculateJobMatch(job, user) {
  if (!user || !job) return { score: 0, fitsPreferences: false, isRecommended: false, shouldDisplay: true };

  // Parse user schema properties safely
  const jobPrefs = user.job_preferences || {};
  const profBg = user.professional_background || {};
  
  // Generate a random score between 40 and 98 for now
  const score = Math.floor(Math.random() * (98 - 40 + 1)) + 40;

  // LOGIC FOR DISPLAY
  // With random scores, we'll just say everything > 90 is recommended and everything is displayed
  const fitsPreferences = true;
  const isRecommended = score > 90;
  const shouldDisplay = true;

  return {
    score,
    fitsPreferences,
    isRecommended,
    shouldDisplay
  };
}
