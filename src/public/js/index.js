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

    // Remove the corresponding hidden input when the button is deselected
    var serverUrl = button.getAttribute('value');
    var hiddenInputs = document.querySelectorAll('input[name="url"][value="' + serverUrl + '"]');
    hiddenInputs.forEach(function (input) {
      input.parentNode.removeChild(input);
    });
  }
}