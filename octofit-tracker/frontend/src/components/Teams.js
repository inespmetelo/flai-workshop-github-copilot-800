import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        setLoading(true);
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
        console.log('Teams API endpoint:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Teams fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setError(null);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
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

  return (
    <div className="container mt-5">
      <div className="mb-4">
        <h1 className="display-5">
          <i className="bi bi-people me-2"></i>Teams
        </h1>
        <p className="text-muted">View and manage fitness teams</p>
      </div>

      <div className="mb-3">
        <button className="btn btn-primary">
          <i className="bi bi-plus-circle me-2"></i>Create New Team
        </button>
      </div>
      
      <div className="row">
        {teams.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              <h5>No teams found</h5>
              <p className="mb-0">Create your first team to get started!</p>
            </div>
          </div>
        ) : (
          teams.map((team) => (
            <div key={team.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header">
                  <h5 className="mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text text-muted">{team.description}</p>
                  <div className="d-flex justify-content-between align-items-center mt-3">
                    <div>
                      <span className="badge bg-info me-2">
                        <i className="bi bi-people-fill me-1"></i>
                        {team.member_count || 0} Members
                      </span>
                    </div>
                  </div>
                </div>
                <div className="card-footer bg-transparent border-top-0">
                  <small className="text-muted">
                    <i className="bi bi-calendar-event me-1"></i>
                    Created: {new Date(team.created_at).toLocaleDateString()}
                  </small>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Teams;
