import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Leaderboard API endpoint:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setError(null);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
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

  const getRankBadgeClass = (rank) => {
    if (rank === 1) return 'rank-badge rank-1';
    if (rank === 2) return 'rank-badge rank-2';
    if (rank === 3) return 'rank-badge rank-3';
    return 'rank-badge rank-other';
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="container mt-5">
      <div className="mb-4">
        <h1 className="display-5">
          <i className="bi bi-trophy-fill me-2"></i>Leaderboard
        </h1>
        <p className="text-muted">Top performers and their achievements</p>
      </div>
      
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th scope="col" style={{width: '80px'}}>Rank</th>
              <th scope="col">User</th>
              <th scope="col">Total Points</th>
              <th scope="col">Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center py-5">
                  <div className="text-muted">
                    <h5>No leaderboard data found</h5>
                    <p>Complete activities to appear on the leaderboard!</p>
                  </div>
                </td>
              </tr>
            ) : (
              leaderboard.map((entry, index) => {
                const rank = index + 1;
                return (
                  <tr key={entry.id || index} className={rank <= 3 ? 'table-light' : ''}>
                    <td>
                      <div className={getRankBadgeClass(rank)}>
                        {getRankIcon(rank)}
                      </div>
                    </td>
                    <td>
                      <strong>{entry.user_name || entry.user}</strong>
                    </td>
                    <td>
                      <span className="badge bg-warning text-dark fs-6">
                        <i className="bi bi-star-fill me-1"></i>
                        {entry.total_points || 0} pts
                      </span>
                    </td>
                    <td>
                      <span className="badge bg-info">
                        <i className="bi bi-activity me-1"></i>
                        {entry.total_activities || 0}
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
      
      {leaderboard.length > 0 && (
        <div className="mt-4">
          <div className="alert alert-info" role="alert">
            <i className="bi bi-info-circle-fill me-2"></i>
            <strong>Keep going!</strong> Complete more activities to climb the leaderboard.
          </div>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
