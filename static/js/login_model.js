window.onload = function () {
  // Get the current URL
  var currentUrl = window.location.href;

  // Extract the `next` parameter from the URL
  var urlParams = new URLSearchParams(window.location.search);
  var nextParam = urlParams.get("next");

  // Update the `next` field in the form if `next` parameter exists
  if (nextParam) {
    document.getElementById("next").value = nextParam;
  }

  // List of URLs where the login modal should appear
  var triggerUrls = ["/book_table/", "/feedback/", "/login"]; // Add more URLs as needed

  // Check if the current URL matches any of the trigger URLs
  triggerUrls.forEach(function (url) {
    if (currentUrl.includes(url)) {
      // Trigger the modal to show automatically
      var myModal = new bootstrap.Modal(document.getElementById("loginModal"), {
        keyboard: false, // Optional: Disable closing the modal with the keyboard
      });
      myModal.show();
    }
  });
};
