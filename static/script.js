// Function to fetch sounds
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

// Function to delete sound
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

// Function to handle volume control
document.addEventListener('DOMContentLoaded', function() {
    const volumeControl = document.getElementById('volumeControl');

    volumeControl.addEventListener('input', function() {
        const volume = parseFloat(this.value) / 100; // Convert to decimal
        setVolume(volume);
    });

    // Function to set volume
    function setVolume(volume) {
        fetch('/volume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ volume: volume })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        })
        .catch(error => {
            console.error('There was a problem with the volume control:', error);
        });
    }
});

// Initial fetch of sounds when the page loads
document.addEventListener('DOMContentLoaded', fetchSounds);

document.addEventListener('DOMContentLoaded', function() {
    const volumeControl = document.getElementById('volumeControl');
    const volumeDisplay = document.getElementById('volumeDisplay');

    volumeControl.addEventListener('input', function() {
        const minAlias = volumeControl.getAttribute('data-min-alias');
        const maxAlias = volumeControl.getAttribute('data-max-alias');
        const value = volumeControl.value;
        volumeDisplay.textContent = value === '0' ? minAlias : value === '100' ? maxAlias : value;
    });
});