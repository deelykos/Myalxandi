function toggleStatus(button) {
    const isCompleted = button.innerHTML === 'Completed';

    if (isCompleted) {
        button.style.backgroundColor = '';
        button.innerHTML = 'Uncompleted';
    } else {
        button.style.backgroundColor = 'green';
        button.innerHTML = 'Completed';
    }
}
