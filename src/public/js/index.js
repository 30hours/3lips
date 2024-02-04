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

function addNewServer() {
  const container = document.getElementById("new-server-container");

  // Create a new text field
  const textField = document.createElement("input");
  textField.type = "text";
  textField.placeholder = "Enter new server name";
  textField.classList.add("form-control", "new-server-field");

  // Create Submit and Cancel buttons
  const submitBtn = document.createElement("button");
  submitBtn.innerText = "Submit";
  submitBtn.classList.add("btn", "btn-success", "w-100", "mb-1");
  submitBtn.onclick = submitNewServer;

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.classList.add("btn", "btn-danger", "w-100", "mb-1");
  cancelBtn.onclick = cancelNewServer;

  // Append elements to the container
  container.innerHTML = ""; // Clear previous content
  container.appendChild(textField);
  container.appendChild(submitBtn);
  container.appendChild(cancelBtn);
}

function submitNewServer(event) {

  event.preventDefault(); 

  const container = document.getElementById("new-server-container");
  const textField = container.querySelector(".new-server-field");

  // Get the entered value
  const serverName = textField.value;

  // Validate if the serverName is not empty
  if (serverName.trim() === "") {
    alert("Please enter a valid server name.");
    return;
  }

  // Create a new button for the server
  const serverBtn = document.createElement("button");
  serverBtn.type = "button";
  serverBtn.classList.add("btn", "btn-success", "toggle-button", "active", "w-100", "mb-1");
  serverBtn.dataset.toggle = "button";
  serverBtn.setAttribute("aria-pressed", "true");
  serverBtn.setAttribute("server-url", serverName);
  serverBtn.innerText = serverName;
  serverBtn.onclick = function () {
    toggle_button(this);
  };

  // Create a hidden input to store the server URL
  const hiddenInput = document.createElement("input");
  hiddenInput.type = "hidden";
  hiddenInput.name = "url";
  hiddenInput.value = serverName;

  // Append the button and input to the server list
  const serverList = document.querySelector("#server-list");
  serverList.appendChild(serverBtn);
  serverList.appendChild(hiddenInput);

  // Clear the new server container
  container.innerHTML = "";
}

function cancelNewServer() {
  const container = document.getElementById("new-server-container");
  container.innerHTML = "";
}