function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const form = document.getElementById('search-form');
const statusEl = document.getElementById('results-status');
const listEl = document.getElementById('results-list');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const matieresSelect = document.getElementById('matieres');
  const matieres = Array.from(matieresSelect.selectedOptions).map(opt => opt.value);
  const heure = document.getElementById('heure').value;
  const jour = document.getElementById('jour').value;
  const filiere = document.getElementById('filiere').value;

  if (matieres.length === 0) {
    statusEl.textContent = 'Veuillez sélectionner au moins une matière.';
    statusEl.className = 'results-status error';
    return;
  }

  statusEl.textContent = 'Recherche en cours...';
  statusEl.className = 'results-status';
  listEl.innerHTML = '';

  try {
    const response = await fetch('/api/rechercher/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ matieres, heure, jour, filiere }),
    });

    const data = await response.json();

    if (!response.ok) {
      statusEl.textContent = data.erreur || 'Une erreur est survenue.';
      statusEl.className = 'results-status error';
      return;
    }

    afficherResultats(data.resultats);
  } catch (err) {
    statusEl.textContent = 'Impossible de contacter le serveur.';
    statusEl.className = 'results-status error';
  }
});

function afficherResultats(resultats) {
  if (resultats.length === 0) {
    statusEl.textContent = 'Aucun mentor compatible trouvé pour ces critères.';
    statusEl.className = 'results-status';
    listEl.innerHTML = '';
    return;
  }

  statusEl.textContent = `${resultats.length} mentor(s) compatible(s) trouvé(s).`;
  statusEl.className = 'results-status';

  listEl.innerHTML = resultats.map(mentor => `
    <article class="mentor-card">
      <div class="mentor-card-header">
        <h3>${escapeHtml(mentor.nom)}</h3>
        <span class="score-badge">${mentor.score}% compatible</span>
      </div>
      <p>Filière : ${escapeHtml(mentor.filiere)} — ${escapeHtml(mentor.niveau)}</p>
      <p>Format : ${escapeHtml(mentor.format_mentorat)}</p>
      <p>Disponibilité correspondante : ${escapeHtml(mentor.disponibilite)}</p>
      <p>Matières en commun :
        ${mentor.matieres_communes.map(m => `<span class="tag">${escapeHtml(m)}</span>`).join('')}
      </p>
    </article>
  `).join('');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
