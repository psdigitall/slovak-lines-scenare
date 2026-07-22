(() => {
  'use strict';

  const forms = document.querySelectorAll('[data-distribution-form]');
  if (!forms.length) return;

  function scenarioId() {
    const fileName = decodeURIComponent(window.location.pathname.split('/').pop() || document.title);
    return fileName.replace(/\.html?$/i, '') || 'scenario';
  }

  forms.forEach((form) => {
    const inputs = Array.from(form.querySelectorAll('input[name="distribution"]'));
    const summary = form.querySelector('[data-distribution-summary]');
    const saveStatus = form.querySelector('[data-distribution-save-status]');
    if (!inputs.length || !summary || !saveStatus) return;

    const storageKey = `sl-scenario-distribution:${scenarioId()}`;
    const allowedValues = new Set(inputs.map((input) => input.value));

    function selectedInputs() {
      return inputs.filter((input) => input.checked);
    }

    function paint() {
      const selected = selectedInputs();
      summary.textContent = selected.length
        ? selected.map((input) => input.dataset.summaryLabel || input.value).join(' · ')
        : 'Nie je vybraná žiadna kampaň ani anglická mutácia.';
      form.classList.toggle('has-selection', selected.length > 0);
    }

    function save() {
      const selected = selectedInputs().map((input) => input.value);
      try {
        localStorage.setItem(storageKey, JSON.stringify({version: 1, selected, updatedAt: new Date().toISOString()}));
        saveStatus.textContent = 'Výber uložený v tomto prehliadači';
      } catch (error) {
        saveStatus.textContent = 'Výber sa nepodarilo uložiť';
      }
      paint();
    }

    function load() {
      try {
        const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
        if (saved && Array.isArray(saved.selected)) {
          const selected = new Set(saved.selected.filter((value) => allowedValues.has(value)));
          inputs.forEach((input) => { input.checked = selected.has(input.value); });
          saveStatus.textContent = 'Načítaný uložený výber';
        } else {
          saveStatus.textContent = 'Predvolený výber podľa zadania';
        }
      } catch (error) {
        saveStatus.textContent = 'Lokálne ukladanie nie je dostupné';
      }
      paint();
    }

    inputs.forEach((input) => input.addEventListener('change', save));
    window.addEventListener('storage', (event) => {
      if (event.key === storageKey) load();
    });
    load();
  });
})();
