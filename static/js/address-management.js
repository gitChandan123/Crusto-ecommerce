// Clear modal input fields when adding a new address
function clearModal() {
  document.getElementById("addressId").value = "";
  document.getElementById("id_user_name").value = "";
  document.getElementById("id_mobile_number").value = "";
  document.getElementById("id_city").value = "";
  document.getElementById("id_state").value = "";
  document.getElementById("id_postal_code").value = "";
  document.getElementById("id_country").value = "";
}

// Populate modal with data for editing an existing address
function editAddress(id, name, mobile_number, city, state, zip_code, country) {
  document.getElementById("addressId").value = id;
  document.getElementById("id_user_name").value = name;
  document.getElementById("id_mobile_number").value = mobile_number;
  document.getElementById("id_city").value = city;
  document.getElementById("id_state").value = state;
  document.getElementById("id_postal_code").value = zip_code;
  document.getElementById("id_country").value = country;
}

// Handle address deletion
function deleteAddress(id) {
  fetch(`/delete_address/${id}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("address-" + id).remove();
        showToastMessage("Address deleted successfully!", "success");
      } else {
        showToastMessage("Failed to delete address.", "error");
      }
    })
    .catch(() => {
      showToastMessage("An error occurred while deleting.", "error");
    });
}

// Function to show a floating toast message
function showToastMessage(message, type) {
  let toast = document.createElement("div");
  toast.innerText = message;
  toast.classList.add("toast-message", type);
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 500);
  }, 2000);
}

// Add basic styles for toast messages
const toastStyles = document.createElement("style");
toastStyles.innerHTML = `
  .toast-message {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #28a745; /* Success default */
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: opacity 0.5s ease-in-out;
    z-index: 1000;
  }
  
  .toast-message.error {
    background-color: #dc3545;
  }

  .toast-message.fade-out {
    opacity: 0;
  }
`;
document.head.appendChild(toastStyles);
