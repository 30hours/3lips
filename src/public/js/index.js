function toggle_button(button) {
  button.classList.toggle('active');
  var pressed = button.getAttribute('aria-pressed') === 'false' ? 'true' : 'false';
  button.setAttribute('aria-pressed', pressed);

  // fix button states
  if (pressed === 'true') {
    button.classList.add("btn-success");
    button.classList.remove("btn-secondary");
  } else {
    button.classList.add("btn-secondary");
    button.classList.remove("btn-success");
  }

  // Set the value to server.url when the button is pressed
  var serverUrl = button.getAttribute('value');
  button.value = pressed === 'true' ? serverUrl : '';
  console.log(button.value);
}
