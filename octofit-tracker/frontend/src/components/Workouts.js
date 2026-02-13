import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        setLoading(true);
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Workouts API endpoint:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setError(null);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-container">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const getDifficultyBadge = (difficulty) => {
    const difficultyLower = (difficulty || '').toLowerCase();
    if (difficultyLower === 'beginner' || difficultyLower === 'easy') {
      return 'bg-success';
    } else if (difficultyLower === 'intermediate' || difficultyLower === 'medium') {
      return 'bg-warning text-dark';
    } else if (difficultyLower === 'advanced' || difficultyLower === 'hard') {
      return 'bg-danger';
    }
    return 'bg-secondary';
  };

  return (
    <div className="container mt-5">
      <div className="mb-4">
        <h1 className="display-5">
          <i className="bi bi-lightning-charge-fill me-2"></i>Workout Suggestions
        </h1>
        <p className="text-muted">Personalized workout recommendations to help you reach your goals</p>
      </div>
      
      <div className="row">
        {workouts.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              <h5>No workouts available</h5>
              <p className="mb-0">Check back later for personalized workout suggestions!</p>
            </div>
          </div>
        ) : (
          workouts.map((workout) => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header">
                  <h5 className="mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text text-muted">{workout.description}</p>
                  
                  <div className="mt-3">
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <span className="text-muted">
                        <i className="bi bi-tag-fill me-1"></i>Type:
                      </span>
                      <span className="badge bg-primary">{workout.workout_type}</span>
                    </div>
                    
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <span className="text-muted">
                        <i className="bi bi-clock-fill me-1"></i>Duration:
                      </span>
                      <strong>{workout.duration} min</strong>
                    </div>
                    
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <span className="text-muted">
                        <i className="bi bi-speedometer2 me-1"></i>Difficulty:
                      </span>
                      <span className={`badge ${getDifficultyBadge(workout.difficulty_level)}`}>
                        {workout.difficulty_level}
                      </span>
                    </div>
                    
                    <div className="d-flex justify-content-between align-items-center">
                      <span className="text-muted">
                        <i className="bi bi-fire me-1"></i>Calories:
                      </span>
                      <span className="badge bg-danger">{workout.calories_estimate} cal</span>
                    </div>
                  </div>
                </div>
                <div className="card-footer bg-transparent border-top-0">
                  <button className="btn btn-primary btn-sm w-100">
                    <i className="bi bi-play-fill me-1"></i>Start Workout
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      
      {workouts.length > 0 && (
        <div className="mt-4">
          <button className="btn btn-info">
            <i className="bi bi-arrow-clockwise me-2"></i>Get New Suggestions
          </button>
        </div>
      )}
    </div>
  );
}

export default Workouts;
