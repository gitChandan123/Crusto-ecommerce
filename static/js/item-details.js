document
  .getElementById("review-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const rating = document.getElementById("rating").value;
    const comment = document.getElementById("comment").value;
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("{% url 'add_review' item.id %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ rating: rating, comment: comment }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const reviewList = document.getElementById("review-list");
          const newReview = document.createElement("div");
          newReview.classList.add(
            "review-item",
            "p-3",
            "mb-3",
            "border",
            "rounded",
            "shadow-sm"
          );
          newReview.innerHTML = `
                <div class="d-flex align-items-center">
                    <strong class="me-2">${data.username}</strong>  
                    <span class="text-warning">⭐ ${data.rating}/5</span>
                </div>
                <p class="text-muted mb-1">${data.comment}</p>
                <small class="text-secondary">${data.created_at}</small>
            `;
          reviewList.prepend(newReview);
          document.getElementById("review-form").reset();
        } else {
          alert("Failed to submit review.");
        }
      });
  });
document
  .getElementById("review-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const rating = document.getElementById("rating").value;
    const comment = document.getElementById("comment").value;
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("{% url 'add_review' item.id %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ rating: rating, comment: comment }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const reviewList = document.getElementById("review-list");
          const newReview = document.createElement("div");
          newReview.classList.add(
            "review-item",
            "p-3",
            "mb-3",
            "border",
            "rounded",
            "shadow-sm"
          );
          newReview.setAttribute("id", "review-" + data.id);
          newReview.innerHTML = `
                <div class="d-flex align-items-center">
                    <strong class="me-2">${data.username}</strong>  
                    <span class="text-warning">⭐ <span class="review-rating">${data.rating}</span>/5</span>
                </div>
                <p class="text-muted mb-1 review-comment">${data.comment}</p>
                <small class="text-secondary">${data.created_at}</small>
                <div class="mt-2">
                    <button class="btn btn-sm btn-outline-primary edit-review" data-review-id="${data.id}" data-rating="${data.rating}" data-comment="${data.comment}">Edit</button>
                    <button class="btn btn-sm btn-outline-danger delete-review" data-review-id="${data.id}">Delete</button>
                </div>
            `;
          reviewList.prepend(newReview);
          document.getElementById("review-form").reset();
        } else {
          alert("Failed to submit review.");
        }
      });
  });

// Handle Edit Review
document.addEventListener("click", function (event) {
  if (event.target.classList.contains("edit-review")) {
    const reviewId = event.target.getAttribute("data-review-id");
    const currentRating = event.target.getAttribute("data-rating");
    const currentComment = event.target.getAttribute("data-comment");

    const newComment = prompt("Edit your review:", currentComment);
    if (!newComment) return;

    fetch(`/update_review/${reviewId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      body: JSON.stringify({ rating: currentRating, comment: newComment }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.querySelector(
            `#review-${reviewId} .review-comment`
          ).textContent = data.comment;
        } else {
          alert("Failed to update review.");
        }
      });
  }
});

// Handle Delete Review
document.addEventListener("click", function (event) {
  if (event.target.classList.contains("delete-review")) {
    const reviewId = event.target.getAttribute("data-review-id");

    fetch(`/delete_review/${reviewId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.getElementById(`review-${reviewId}`).remove();
        } else {
          alert("Failed to delete review.");
        }
      });
  }
});
