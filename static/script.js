function fetchSounds() {
    fetch('/list_sounds')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('soundSelect');
            select.innerHTML = '';
            data.forEach(sound => {
                const option = document.createElement('option');
                option.value = sound;
                option.text = sound;
                select.appendChild(option);
            });
        });
}

function deleteSound() {
    const filename = document.getElementById('soundSelect').value;
    fetch('/delete/' + filename, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                fetchSounds();
                alert(data.message);
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchSounds();
});
