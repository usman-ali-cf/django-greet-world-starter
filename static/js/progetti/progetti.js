/*  Tabella progetti in stile DataTable (stessi helper di crea_nodo)  */

import { renderDataTable } from '../standard/tables.js';   // ⬅️ già esiste
import { apiFetch }       from '../standard/api.js';       // ⬅️ già esiste

/* colonne per la DataTable */
const columnsProgetti = [
  { header: "Nome progetto", field: "nome" },
  { header: "Descrizione",   field: "descrizione" },
  { header: "Azioni",        field: "id_prg" }          // contenuto sostituito dopo il render
];

document.addEventListener("DOMContentLoaded", () => {
  /* --------- DOM --------- */
  const TBody       = document.getElementById("listaProgetti");
  const BTN_NEW     = document.getElementById("btnNuovoProgetto");
  const BTN_REFRESH = document.getElementById("btnAggiornaProgetti");

  /* --------- POP-UP --------- */
  const POPUP      = document.getElementById("popupNuovoProj");
  const BTN_CLOSE  = document.getElementById("btnChiudiPopup");
  const FORM       = document.getElementById("formNuovoProgetto");
  const INP_NOME   = document.getElementById("inpNomeProj");
  const TXT_DESC   = document.getElementById("txtDescProj");

  const openPopup  = () => { POPUP.style.display = "flex"; INP_NOME.focus(); };
  const closePopup = () => { POPUP.style.display = "none"; FORM.reset(); };

  /* --------- LOAD / RENDER --------- */
  async function loadProgetti() {
    try {
      const data = await apiFetch("/api/progetti");
      renderDataTable({
        containerSelector : "#listaProgetti",
        columns           : columnsProgetti,
        data,
        /* click riga – opzionale: selezione visiva */
        onRowClick        : (_, tr) => {
          tr.parentNode.querySelectorAll('tr')
            .forEach(r => r.classList.remove('selected'));
          tr.classList.add('selected');
        }
      });

      // sostituisco la colonna “Azioni” con i pulsanti
      addActionButtons(data);
    } catch (err) {
      console.error(err);
      TBody.innerHTML =
        `<tr><td colspan="3">Errore nel caricamento</td></tr>`;
    }
  }

  function addActionButtons(progetti) {
    const rows = TBody.querySelectorAll('tr');
    rows.forEach((row, idx) => {
      const proj = progetti[idx];
      const td   = row.lastElementChild;          // colonna “Azioni”

      /* crea pulsante APRI */
      const btnOpen = document.createElement("button");
      btnOpen.textContent = "Apri";
      btnOpen.className   = "btn-apri";
      btnOpen.addEventListener("click", () => {
        window.location.href = proj.url_dettaglio;    // l’API già fornisce l’URL
      });

      /* crea pulsante ELIMINA */
      const btnDel = document.createElement("button");
      btnDel.textContent = "Elimina";
      btnDel.className   = "btn-elimina";
      btnDel.style.marginLeft = "6px";
      btnDel.addEventListener("click", () => deleteProject(proj.id_prg, proj.nome));

      td.style.textAlign = "center";
      td.innerHTML = "";                 // pulisco cella
      td.append(btnOpen, btnDel);
    });
  }

  /* --------- CRUD --------- */
  async function createProject(payload) {
    await apiFetch("/api/progetti", {
      method : "POST",
      body   : JSON.stringify(payload),
      headers: { "Content-Type": "application/json" }
    });
  }

  async function deleteProject(id, nome) {
    if (!confirm(`Eliminare il progetto «${nome}»?`)) return;
    await apiFetch(`/api/progetti/${id}`, { method: "DELETE" });
    loadProgetti();
  }

  /* --------- EVENTI --------- */
  BTN_NEW    .addEventListener("click", openPopup);
  BTN_CLOSE  .addEventListener("click", closePopup);
  BTN_REFRESH.addEventListener("click", loadProgetti);
  window.addEventListener("keyup", e => {
    if (e.key === "Escape" && POPUP.style.display === "flex") closePopup();
  });

  /* submit popup */
  FORM.addEventListener("submit", async e => {
    e.preventDefault();
    const nome = INP_NOME.value.trim();
    const desc = TXT_DESC.value.trim();
    if (!nome || !desc) return;
    await createProject({ nome_progetto: nome, descrizione_progetto: desc });
    closePopup();
    loadProgetti();
  });

  /* primo caricamento */
  loadProgetti();
});
