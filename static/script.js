const form = document.querySelector('#plan-form');
const packButtons = document.querySelectorAll('.pill-select');
const packInput = document.querySelector('input[name="pack"]');

const summary = {
  pack: document.querySelector('#summary-pack'),
  interval: document.querySelector('#summary-interval'),
  size: document.querySelector('#summary-size'),
  email: document.querySelector('#summary-email'),
  title: document.querySelector('#summary-title'),
  subtitle: document.querySelector('#summary-subtitle')
};

packButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    packButtons.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    const value = btn.dataset.value;
    packInput.value = value;
    summary.pack.textContent = `${value} pack`;
    updateTitle();
  });
});

if (form) {
  form.addEventListener('change', () => {
    const interval = form.elements['interval']?.value;
    const size = form.elements['size']?.value;
    const email = form.elements['email']?.value;

    summary.interval.textContent = interval || '—';
    summary.size.textContent = size || '—';
    summary.email.textContent = email || '—';
    updateTitle();
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    updateTitle(true);
    form.querySelector('button[type="submit"]').textContent = 'Reserved';
  });
}

function updateTitle(confirmed = false) {
  const pack = packInput?.value;
  const interval = form?.elements['interval']?.value;
  const size = form?.elements['size']?.value;

  if (pack && interval && size) {
    summary.title.textContent = confirmed ? 'Reserved. You are set.' : 'Ready to confirm.';
    summary.subtitle.textContent = `${pack} pack • ${interval} • ${size}`;
  } else {
    summary.title.textContent = 'Choose a pack';
    summary.subtitle.textContent = 'Pick your batch size, interval, and fit to see your plan.';
  }
}

