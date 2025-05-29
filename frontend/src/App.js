
import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState('');

  const searchMovie = async () => {
    if (!query) return;
    try {
      const res = await fetch(`https://movie-sug.onrender.com/movie-info?title=${query}`);
      const data = await res.json();
      if (data.error) {
        setError(data.error);
        setMovie(null);
      } else {
        setMovie(data);
        setError('');
      }
    } catch (err) {
      setError('مشکلی در ارتباط با سرور پیش آمد');
    }
  };

  return (
    <div className="App">
      <h1>جستجوی فیلم</h1>
      <input
        type="text"
        placeholder="نام فیلم را وارد کنید"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={searchMovie}>جستجو</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {movie && (
        <div className="movie-card">
          <h2>{movie.title}</h2>
          {movie.poster_path && <img src={movie.poster_path} alt={movie.title} width="200" />}
          <p><strong>ژانر:</strong> {movie.genres.join(', ')}</p>
          <p><strong>خلاصه:</strong> {movie.overview}</p>

          {movie.similar && movie.similar.length > 0 && (
            <div>
              <h3>فیلم‌های مشابه:</h3>
              <div className="similar-movies">
                {movie.similar.map((sim, index) => (
                  <div key={index} className="similar-movie">
                    {sim.poster_path && <img src={sim.poster_path} alt={sim.title} width="100" />}
                    <p>{sim.title}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
