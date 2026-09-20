function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

const CSRF_TOKEN = getCookie("csrftoken");

async function apiPost(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN,
    },
    body: JSON.stringify(data || {}),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Request failed (${res.status})`);
  }
  return res.json();
}

// ---------------------------------------------------------------------------
// Quest toggling (dashboard)
// ---------------------------------------------------------------------------

function initQuestToggles() {
  document.querySelectorAll("[data-quest-item]").forEach((item) => {
    item.addEventListener("click", async () => {
      const questId = parseInt(item.dataset.questItem, 10);
      try {
        const result = await apiPost("/api/quest/toggle/", { quest_id: questId });
        item.classList.toggle("done", result.completed);
        const box = item.querySelector("[data-quest-checkbox]");
        if (box) box.textContent = result.completed ? "✓" : "";

        const counter = document.querySelector("[data-quest-counter]");
        if (counter) counter.textContent = `${result.quests_done}/${result.quests_total}`;
      } catch (err) {
        console.error(err);
      }
    });
  });
}

// ---------------------------------------------------------------------------
// Accountability / scold modal
// ---------------------------------------------------------------------------

function initScoldModal() {
  const overlay = document.querySelector("[data-scold-modal]");
  if (!overlay) return;

  const dismissBtn = overlay.querySelector("[data-scold-dismiss]");
  if (dismissBtn) {
    dismissBtn.addEventListener("click", async () => {
      const targetDate = overlay.dataset.scoldDate;
      try {
        await apiPost("/api/scold/dismiss/", { date: targetDate });
      } catch (err) {
        console.error(err);
      }
      overlay.setAttribute("hidden", "hidden");
    });
  }
}

// ---------------------------------------------------------------------------
// Weight form (Body tab)
// ---------------------------------------------------------------------------

function initWeightForm() {
  const form = document.querySelector("[data-weight-form]");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = form.querySelector("[name=weight_kg]");
    const value = parseFloat(input.value);
    if (!value) return;

    try {
      const result = await apiPost("/api/weight/", { weight_kg: value });
      window.location.reload();
    } catch (err) {
      const errorEl = form.querySelector("[data-form-error]");
      if (errorEl) errorEl.textContent = err.message;
    }
  });
}

// ---------------------------------------------------------------------------
// Trading form (Money tab)
// ---------------------------------------------------------------------------

function initTradingForm() {
  const form = document.querySelector("[data-trading-form]");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const amount = parseFloat(form.querySelector("[name=amount_usd]").value);
    const dateVal = form.querySelector("[name=date]").value;
    const notes = form.querySelector("[name=notes]")?.value || "";

    if (isNaN(amount)) return;

    try {
      await apiPost("/api/trading/", { amount_usd: amount, date: dateVal, notes });
      window.location.reload();
    } catch (err) {
      const errorEl = form.querySelector("[data-form-error]");
      if (errorEl) errorEl.textContent = err.message;
    }
  });
}

// ---------------------------------------------------------------------------
// Journal form (Log tab)
// ---------------------------------------------------------------------------

function initJournalForm() {
  const form = document.querySelector("[data-journal-form]");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const textarea = form.querySelector("[name=text]");
    const text = textarea.value.trim();
    if (!text) return;

    try {
      await apiPost("/api/journal/", { text });
      window.location.reload();
    } catch (err) {
      const errorEl = form.querySelector("[data-form-error]");
      if (errorEl) errorEl.textContent = err.message;
    }
  });
}

// ---------------------------------------------------------------------------
// PIN input UX — auto-submit style numeric-only field
// ---------------------------------------------------------------------------

function initPinInput() {
  document.querySelectorAll(".pin-input").forEach((input) => {
    input.addEventListener("input", () => {
      input.value = input.value.replace(/\D/g, "").slice(0, 4);
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initQuestToggles();
  initScoldModal();
  initWeightForm();
  initTradingForm();
  initJournalForm();
  initPinInput();
});
