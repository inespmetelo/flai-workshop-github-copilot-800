import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-gradient">
        <div className="container-fluid">
          <Link className="navbar-brand d-flex align-items-center" to="/">
            <img 
              src="/octofitapp-logo.png" 
              alt="OctoFit Logo" 
              height="40" 
              className="me-2 logo-image"
            />
            <span className="brand-text">OctoFit Tracker</span>
          </Link>
          <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav" 
            aria-controls="navbarNav" 
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/users">Users</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/teams">Teams</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/activities">Activities</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/workouts">Workouts</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={
          <div className="container mt-5">
            <div className="hero-section mb-5">
              <div className="hero-blob blob-1"></div>
              <div className="hero-blob blob-2"></div>
              <div className="hero-blob blob-3"></div>
              
              <div className="jumbotron text-center position-relative">
                <div className="hero-icon mb-4">
                  <i className="bi bi-heart-pulse-fill"></i>
                </div>
                <h1 className="display-3 mb-4 animate-fade-in">
                  Welcome to OctoFit Tracker
                </h1>
                <p className="lead mt-4 mb-4 animate-fade-in-delay">
                  Track your fitness journey, compete with your team, and achieve your goals!
                </p>
                <hr className="my-4 gradient-hr" />
                <p className="mb-5 subtitle animate-fade-in-delay-2">
                  Join the ultimate fitness tracking experience with real-time leaderboards and personalized workouts
                </p>
                
                <div className="d-grid gap-3 d-md-flex justify-content-md-center mb-5">
                  <Link to="/activities" className="btn btn-primary btn-lg btn-modern">
                    <i className="bi bi-plus-circle me-2"></i>Log Activity
                  </Link>
                  <Link to="/leaderboard" className="btn btn-success btn-lg btn-modern">
                    <i className="bi bi-trophy-fill me-2"></i>View Leaderboard
                  </Link>
                  <Link to="/workouts" className="btn btn-warning btn-lg btn-modern">
                    <i className="bi bi-lightning-charge-fill me-2"></i>Get Workouts
                  </Link>
                </div>
              </div>
            </div>

            <div className="row g-4 mt-5">
              <div className="col-md-4 mb-4">
                <div className="feature-card">
                  <div className="feature-icon-wrapper">
                    <div className="feature-icon bg-gradient-blue">
                      <i className="bi bi-activity"></i>
                    </div>
                  </div>
                  <h5 className="card-title mt-4">Track Activities</h5>
                  <p className="card-text text-muted">
                    Log your workouts and monitor your progress over time with detailed analytics.
                  </p>
                  <Link to="/activities" className="btn btn-link">
                    Explore Activities <i className="bi bi-arrow-right ms-2"></i>
                  </Link>
                </div>
              </div>
              
              <div className="col-md-4 mb-4">
                <div className="feature-card">
                  <div className="feature-icon-wrapper">
                    <div className="feature-icon bg-gradient-green">
                      <i className="bi bi-people"></i>
                    </div>
                  </div>
                  <h5 className="card-title mt-4">Join Teams</h5>
                  <p className="card-text text-muted">
                    Connect with others and compete together for fitness goals and achievements.
                  </p>
                  <Link to="/teams" className="btn btn-link">
                    View Teams <i className="bi bi-arrow-right ms-2"></i>
                  </Link>
                </div>
              </div>
              
              <div className="col-md-4 mb-4">
                <div className="feature-card">
                  <div className="feature-icon-wrapper">
                    <div className="feature-icon bg-gradient-orange">
                      <i className="bi bi-lightning-charge-fill"></i>
                    </div>
                  </div>
                  <h5 className="card-title mt-4">Get Workouts</h5>
                  <p className="card-text text-muted">
                    Discover personalized workout suggestions tailored for your fitness level.
                  </p>
                  <Link to="/workouts" className="btn btn-link">
                    Browse Workouts <i className="bi bi-arrow-right ms-2"></i>
                  </Link>
                </div>
              </div>
            </div>

            <div className="row mt-5 mb-5">
              <div className="col-12">
                <div className="stats-banner">
                  <div className="row text-center">
                    <div className="col-md-3 col-6 mb-3">
                      <div className="stat-item">
                        <i className="bi bi-people-fill stat-icon"></i>
                        <h3 className="stat-number">10+</h3>
                        <p className="stat-label">Active Users</p>
                      </div>
                    </div>
                    <div className="col-md-3 col-6 mb-3">
                      <div className="stat-item">
                        <i className="bi bi-activity stat-icon"></i>
                        <h3 className="stat-number">50+</h3>
                        <p className="stat-label">Activities Logged</p>
                      </div>
                    </div>
                    <div className="col-md-3 col-6 mb-3">
                      <div className="stat-item">
                        <i className="bi bi-trophy-fill stat-icon"></i>
                        <h3 className="stat-number">2</h3>
                        <p className="stat-label">Teams Competing</p>
                      </div>
                    </div>
                    <div className="col-md-3 col-6 mb-3">
                      <div className="stat-item">
                        <i className="bi bi-lightning-charge-fill stat-icon"></i>
                        <h3 className="stat-number">6</h3>
                        <p className="stat-label">Workout Plans</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="row mt-5">
              <div className="col-12">
                <div className="info-card">
                  <div className="row align-items-center">
                    <div className="col-md-2 text-center mb-3 mb-md-0">
                      <i className="bi bi-info-circle-fill info-icon"></i>
                    </div>
                    <div className="col-md-10">
                      <h5 className="mb-3">Ready to start your fitness journey?</h5>
                      <p className="mb-0">
                        Start by logging your first activity, join a team, and watch yourself climb the leaderboard!
                        Complete workouts to earn points and compete with your teammates for glory.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        } />
        <Route path="/users" element={<Users />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/workouts" element={<Workouts />} />
      </Routes>
    </div>
  );
}

export default App;

