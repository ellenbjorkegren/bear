const selects = document.querySelectorAll('.pill-select');
const hiddenInputs = {
  type: document.querySelector('input[name="type"]'),
  size: document.querySelector('input[name="size"]'),
  interval: document.querySelector('input[name="interval"]'),
};

const summary = {
  type: document.querySelector('#summary-type'),
  size: document.querySelector('#summary-size'),
  interval: document.querySelector('#summary-interval'),
  email: document.querySelector('#summary-email'),
};

selects.forEach((btn) => {
  btn.addEventListener('click', () => {
    const group = btn.dataset.group;
    if (group) {
      document.querySelectorAll(`.pill-select[data-group="${group}"]`).forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      hiddenInputs[group].value = btn.dataset.value;
      summary[group].textContent = btn.dataset.value;
    }
  });
});

const emailInput = document.querySelector('input[type="email"]');
if (emailInput) {
  emailInput.addEventListener('input', () => {
    summary.email.textContent = emailInput.value || '—';
  });
}

const form = document.querySelector('form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    if (button) button.textContent = 'Reserved';
  });
}


