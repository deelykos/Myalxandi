// status.js
function toggleStatus(button, taskId) {
    const isCompleted = button.innerHTML === 'Completed';

    // Send a request to the server to update the status
    fetch(`/update_status/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({ completed: !isCompleted }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the button style and text based on the updated status from the server
        if (data.completed) {
            button.style.backgroundColor = 'rgb(9, 167, 9)';
            button.innerHTML = 'Completed';
        } else {
            button.style.backgroundColor = 'beige';
            button.innerHTML = 'Uncompleted';
        }
    })
    .catch(error => console.error('Error updating status:', error));
}
