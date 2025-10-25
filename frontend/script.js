const form = document.getElementById('predict-form');
const fileInput = document.getElementById('file');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const labelEl = document.getElementById('label');
const scoresEl = document.getElementById('scores');
const previewEl = document.getElementById('preview');

function setStatus(msg, isError=false){
  statusEl.textContent = msg;
  statusEl.style.color = isError ? '#fca5a5' : '';
}

function showPreview(file){
  if(!file){ previewEl.innerHTML=''; return; }
  const url = URL.createObjectURL(file);
  previewEl.innerHTML = `<img src="${url}" alt="preview" />`;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if(!file){ setStatus('Please choose an image file.', true); return; }

  showPreview(file);
  setStatus('Predicting...');
  resultEl.classList.add('hidden');
  scoresEl.innerHTML = '';

  const formData = new FormData();
  formData.append('file', file);

  const baseUrl = (window.API_BASE_URL || '').replace(/\/$/, '');
  if(!baseUrl){ setStatus('Configure API_BASE_URL in frontend/config.js to point to your Render backend.', true); return; }

  try{
    const res = await fetch(`${baseUrl}/predict-image`, { method: 'POST', body: formData });
    const data = await res.json();
    if(!res.ok || !data.ok){
      throw new Error(data?.error || `HTTP ${res.status}`);
    }
    labelEl.textContent = data.label;
    scoresEl.innerHTML = '';
    Object.entries(data.scores).forEach(([k,v]) => {
      const li = document.createElement('li');
      li.textContent = `${k}: ${(v*100).toFixed(2)}%`;
      scoresEl.appendChild(li);
    });
    resultEl.classList.remove('hidden');
    setStatus('Done.');
  }catch(err){
    setStatus(`Error: ${err.message}`, true);
  }
});

fileInput.addEventListener('change', () => showPreview(fileInput.files[0]));
