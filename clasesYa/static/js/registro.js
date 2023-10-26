const emailInput = document.querySelector('#inputEmail');
const emailError = document.querySelector('#inputEmail + .error');
const passwordInput = document.querySelector('#inputPassword');
const confirmarPasswordInput = document.querySelector('#inputConfirmarPassword');
const confirmarPasswordError = document.querySelector('#inputConfirmarPassword + .error');
const tipoUsuarioInput = document.querySelector('#selectTipoUsuario');
const termCheckBoxInput = document.querySelector('#termCheckBox');
const privaCheckBoxInput = document.querySelector('#privaCheckBox');
const registrarseButton = document.querySelector('.botonCustom');
registrarseButton.disabled = true;

emailInput.addEventListener('input', () => {
  if (!emailInput.validity.valid) {
    emailError.classList.add('show');
  } else {
    emailError.classList.remove('show');
  }
  checkValidity();
});

confirmarPasswordInput.addEventListener('input', () => {
  if (confirmarPasswordInput.value !== passwordInput.value) {
    confirmarPasswordError.classList.add('show');
    confirmarPasswordError.classList.add('is-invalid');
  } else {
    confirmarPasswordError.classList.remove('show');
    confirmarPasswordError.classList.remove('is-invalid');
  }
  checkValidity();
});

tipoUsuarioInput.addEventListener('change', () => {
  if (tipoUsuarioInput.value !== '1' && tipoUsuarioInput.value !== '2') {
    tipoUsuarioInput.classList.add('is-invalid');
  } else {
    tipoUsuarioInput.classList.remove('is-invalid');
  }
  checkValidity();
});

termCheckBoxInput.addEventListener('change', () => {
  if (!termCheckBoxInput.checked) {
    termCheckBoxInput.classList.add('is-invalid');
  } else {
    termCheckBoxInput.classList.remove('is-invalid');
  }
  checkValidity();
});

privaCheckBoxInput.addEventListener('change', () => {
  if (!privaCheckBoxInput.checked) {
    privaCheckBoxInput.classList.add('is-invalid');
  } else {
    privaCheckBoxInput.classList.remove('is-invalid');
  }
  checkValidity();
});

function checkValidity() {
  const emailValid = emailInput.validity.valid;
  const passwordValid = passwordInput.validity.valid;
  const confirmarPasswordValid = confirmarPasswordInput.validity.valid;
  const tipoUsuarioValid = tipoUsuarioInput.value === '1' || tipoUsuarioInput.value === '2';
  const termCheckBoxValid = termCheckBoxInput.checked;
  const privaCheckBoxValid = privaCheckBoxInput.checked;

  const passwordsMatch = passwordInput.value === confirmarPasswordInput.value;

  if (!emailValid || !passwordValid || !confirmarPasswordValid || !passwordsMatch || !tipoUsuarioValid || !termCheckBoxValid || !privaCheckBoxValid) {
    registrarseButton.disabled = true;
  } else {
    registrarseButton.disabled = false;
  }
}
