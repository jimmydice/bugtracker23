document.getElementById("bugForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  // Convert the form data to a JSON object
  const bugData = {};
  formData.forEach((value, key) => {
      bugData[key] = value;
  });

  // Send a POST request to create a new bug
  fetch("/bugs", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(bugData),
  })
  .then((response) => response.json())
  .then((data) => {
      console.log(data); // For debugging purposes
      // Clear the form after successful submission
      form.reset();
      // Reload the bug list to display the newly created bug
      window.location.reload();
  })
  .catch((error) => {
      console.error("Error creating bug:", error);
  });
});

function editBug(bugId) {
    // Implement this function to handle updating a bug
    // You can use JavaScript's prompt or create a modal for editing the bug details
    const newTitle = prompt("Enter the new title for the bug:");
    const newDescription = prompt("Enter the new description for the bug:");
    const newStatus = prompt("Enter the new status for the bug:");
    const newPriority = prompt("Enter the new priority for the bug:");

    if (newTitle && newDescription && newStatus && newPriority) {
        const updatedData = {
            title: newTitle,
            description: newDescription,  // Add the 'description' field
            status: newStatus,
            priority: newPriority
        };

        // Send a PUT request to the backend API to update the bug data
        fetch(`/bugs/${bugId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedData),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data); // For debugging purposes
            // Reload the bug list after successful update
            window.location.reload();
        })
        .catch((error) => {
            console.error("Error updating bug:", error);
        });
    }
}



function deleteBug(bugId) {
  // Implement this function to handle deleting a bug
  const confirmDelete = confirm("Are you sure you want to delete this bug?");

  if (confirmDelete) {
      // Send a DELETE request to the backend API to delete the bug
      fetch(`/bugs/${bugId}`, {
          method: "DELETE",
      })
      .then((response) => response.json())
      .then((data) => {
          console.log(data); // For debugging purposes
          // Remove the bug row from the table after successful deletion
          const bugRow = document.getElementById(`bugRow_${bugId}`);
          bugRow.remove();
      })
      .catch((error) => {
          console.error("Error deleting bug:", error);
      });
  }
}

document.getElementById("searchForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const keyword = formData.get("keyword");
  const category = formData.get("category");

  // Send a GET request to the backend API to search for bugs
  fetch(`/search?keyword=${keyword}&category=${category}`)
      .then((response) => response.json())
      .then((data) => {
          console.log(data); // For debugging purposes
          // Clear the form after successful search
          form.reset();
          // Update the bug list with the search results
          updateBugList(data);
      })
      .catch((error) => {
          console.error("Error searching for bugs:", error);
      });
});

function updateBugList(bugs) {
  // Function to update the bug listing table with search results
  const bugTableBody = document.querySelector("tbody");
  bugTableBody.innerHTML = "";

  bugs.forEach((bug) => {
      const bugRow = document.createElement("tr");
      bugRow.id = `bugRow_${bug.id}`;

      const titleCell = document.createElement("td");
      titleCell.textContent = bug.title;
      bugRow.appendChild(titleCell);

      const descriptionCell = document.createElement("td");
      descriptionCell.textContent = bug.description;
      bugRow.appendChild(descriptionCell);

      const statusCell = document.createElement("td");
      statusCell.textContent = bug.status;
      bugRow.appendChild(statusCell);

      const priorityCell = document.createElement("td");
      priorityCell.textContent = bug.priority;
      bugRow.appendChild(priorityCell);

      const dateCell = document.createElement("td");
      dateCell.textContent = new Date(bug.date_created).toLocaleString(); // Convert date to local string format
      bugRow.appendChild(dateCell);

      const actionsCell = document.createElement("td");
      const updateButton = document.createElement("button");
      updateButton.classList.add("btn", "btn-sm", "btn-info");
      updateButton.textContent = "Update";
      updateButton.onclick = () => editBug(bug.id);
      actionsCell.appendChild(updateButton);

      const deleteButton = document.createElement("button");
      deleteButton.classList.add("btn", "btn-sm", "btn-danger");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteBug(bug.id);
      actionsCell.appendChild(deleteButton);

      bugRow.appendChild(actionsCell);

      bugTableBody.appendChild(bugRow);
  });
}


document.addEventListener("DOMContentLoaded", function () {
    // Handle the "Delete" button click
    document.getElementById("deleteAccountButton").addEventListener("click", function () {
        // Display the confirmation modal
        $('#confirmDeleteModal').modal('show');
    });

    // Handle the "Confirm Delete" button click
    document.getElementById("confirmDelete").addEventListener("click", function () {
        // Redirect to the delete account route when confirmed
        window.location.href = '/delete-account';
    });
});
