/* static/js/carica_file/carica_file.js
   – Upload file utenze via fetch
   – Se torna HTML di conferma, lo iniettiamo in un modal
   – Caso 2: conferma elimina + ricarica
   – Overlay di attesa comune
*/
document.addEventListener('DOMContentLoaded', () => {
  const overlayUpload = document.getElementById('loadingOverlay');   // ⏳
  const feedback      = document.getElementById('feedback') || creaFeedback();
  const wait          = ms => new Promise(r => setTimeout(r, ms));

  function showOverlay() { overlayUpload.style.display = 'flex'; }
  function hideOverlay() { overlayUpload.style.display = 'none'; }

  // 1) CASO UPLOAD
  const formUpload = document.getElementById('formUploadUtenze');
  if (formUpload) {
    // download template
    document.getElementById('download-template-btn')
      ?.addEventListener('click', () => window.location.href = '/download_template');

    formUpload.addEventListener('submit', async ev => {
      ev.preventDefault();
      if (!formUpload.file_utenze.files.length) return;

      showOverlay();
      const fd = new FormData(formUpload);

      try {
        const resp = await fetch(formUpload.action, { method: 'POST', body: fd });
        const text = await resp.text();

        // SE RITORNA LA PAGINA DI CONFERMA (HTML)
        if (/id="form-conferma"/.test(text)) {
          hideOverlay();
          apriConfirmModal(text);
          return;
        }

        // ALTRIMENTI PROVIAMO A PARSARE JSON
        let json = {};
        try { json = JSON.parse(text); } catch (_) {}

        await wait(500);
        hideOverlay();
        if (resp.ok) {
          feedback.textContent = json.message || 'File caricato con successo.';
          feedback.style.color = 'green';
        } else {
          feedback.textContent = `❌ ${json.message || 'Errore.'}`;
          feedback.style.color = 'red';
        }

      } catch (err) {
        console.error(err);
        await wait(500);
        hideOverlay();
        feedback.textContent = 'Errore di connessione.';
        feedback.style.color = 'red';
      }
    });

    return; // non proseguiamo al caso 2
  }

  // 2) CASO CONFERMA (se il modal è già in pagina, viene gestito in initConfirmModal)
});

// se non esiste <p id="feedback">, lo creiamo
function creaFeedback() {
  const p = document.createElement('p');
  p.id = 'feedback';
  p.className = 'feedback-message';
  document.querySelector('main.container')?.appendChild(p);
  return p;
}

// ========= Modal di conferma =========
function apriConfirmModal(htmlText) {
  // parsare il fragment HTML restituito
  const parser = new DOMParser();
  const doc    = parser.parseFromString(htmlText, 'text/html');
  const main   = doc.querySelector('main.container');
  const loadingOverlay = document.getElementById('loadingOverlay');

  // costruiamo il nostro overlay
  const modalOverlay = document.createElement('div');
  modalOverlay.id    = 'confirmModal';
  modalOverlay.className = 'popup-overlay';
  modalOverlay.innerHTML = `
  <div class="popup-content" style="
       width: 600px;
       max-width: 90%;
       padding: 30px;
       font-size: 16px;
       box-sizing: border-box;
  ">
    ${main.innerHTML}
  </div>
`;
document.body.appendChild(modalOverlay);

  // inizializziamo i listener di conferma/annulla
  initConfirmModal(loadingOverlay, modalOverlay);
}

function initConfirmModal(loadingOverlay, modalOverlay) {
  const btnConferma = modalOverlay.querySelector('#btn-conferma');
  const btnAnnulla  = modalOverlay.querySelector('#btn-annulla');
  const feedback    = modalOverlay.querySelector('#feedback') || creaFeedback();
  const filePath    = modalOverlay.querySelector('#file_path').value;
  const idPrg       = modalOverlay.querySelector('#id_prg').value;
  const wait        = ms => new Promise(r => setTimeout(r, ms));

  function show() { loadingOverlay.style.display = 'flex'; }
  function hide() { loadingOverlay.style.display = 'none'; }

  btnConferma.addEventListener('click', async () => {
    show();
    try {
      const resp = await fetch(`/progetto/${idPrg}/carica_file_utenze`, {
        method : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify({ conferma: true, file_path: filePath })
      });
      const json = await resp.json().catch(() => ({}));
      await wait(500);
      hide();

      if (resp.ok) {
        feedback.textContent = json.message || 'File caricato con successo!';
        feedback.style.color = 'green';
        // chiudiamo il modal e ricarichiamo il form originale dopo 1.5s
        setTimeout(() => {
          document.getElementById('confirmModal')?.remove();
          window.location.href = `/progetto/${idPrg}/carica_file_utenze`;
        }, 1500);

      } else {
        feedback.textContent = `❌ ${json.message || 'Errore.'}`;
        feedback.style.color = 'red';
      }

    } catch (err) {
      console.error(err);
      await wait(500);
      hide();
      feedback.textContent = 'Errore di connessione.';
      feedback.style.color = 'red';
    }
  });

  btnAnnulla.addEventListener('click', () => {
    // semplicemente chiudiamo il modal
    modalOverlay.remove();
  });
}