let uploadedVideoFileName; // Variable to store the uploaded video filename

document.getElementById('videoUpload').addEventListener('change', async function(event) {
	const file = event.target.files[0];
	const formData = new FormData();
	formData.append('video', file);

	try {
		const response = await fetch('/api/videos/upload', {
			method: 'POST',
			body: formData,
		});

		if (response.ok) {
			console.log('Video uploaded successfully');

			const data = await response.text(); // Get the response as plain text
			uploadedVideoFileName = data;// Extract filename from the response
			const videoPlayer = document.getElementById('videoPlayer');
			videoPlayer.src = `/api/videos/download/${uploadedVideoFileName}`;
			// Use the response data to show the video or its thumbnail in the UI
		} else {
			console.error('Upload failed');
		}
	} catch (error) {
		console.error('Error:', error);
	}
});




// Function to handle video cut
document.getElementById('cutBtn').addEventListener('click', async function() {
	const startTime = document.getElementById('startTime').value;
	const endTime = document.getElementById('endTime').value;
	try {
		const response = await fetch('/api/videos/cut', {
			method: 'POST',
			body: JSON.stringify({ fileName: uploadedVideoFileName, startTime, endTime }),
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (response.ok) {
			console.log('Video cut successfully');
			showSuccessMessage('Video cut successfully');
			// Show download button
			document.getElementById('downloadBtn').style.display = 'inline-block';

			// Handle success
		} else {
			console.error('Video cut failed');
			showErrorMessage('Video cut failed');
		}
	} catch (error) {
		console.error('Error:', error);
		showErrorMessage('Video cut failed');
	}
});

// Function to handle video trim
document.getElementById('trimBtn').addEventListener('click', async function() {
	const startTime = document.getElementById('startTime').value;
	const endTime = document.getElementById('endTime').value;

	try {
		const response = await fetch('/api/videos/trim', {
			method: 'POST',
			body: JSON.stringify({ fileName: uploadedVideoFileName, startTime, endTime }),
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (response.ok) {
			console.log('Video trim successfully');
			showSuccessMessage('Video trim successfully');
			// Show download button
			document.getElementById('downloadBtn').style.display = 'inline-block';
			// Handle success
		} else {
			console.error('Video trim failed');
			showErrorMessage('Video trim failed');
		}
	} catch (error) {
		console.error('Error:', error);
		showErrorMessage('Video trim failed');
	}
});


// Example for export button
document.getElementById('exportBtn').addEventListener('click', function() {
	alert('Export functionality will be processed on the backend');
	// Here you would typically send a request to your backend to process the export
});


// Function to download video
document.getElementById('downloadBtn').addEventListener('click', function() {
	if (uploadedVideoFileName) {
		// Construct the download URL with the uploaded video filename
		const downloadUrl = `/api/videos/download/${uploadedVideoFileName}`;
		// Redirect to the download URL
		window.location.href = downloadUrl;
	} else {
		console.error('No uploaded video found');
	}
});

// Function to toggle full screen mode
function toggleFullScreen() {
	const videoPlayer = document.getElementById('videoPlayer');
	if (videoPlayer.requestFullscreen) {
		videoPlayer.requestFullscreen();
	} else if (videoPlayer.mozRequestFullScreen) { /* Firefox */
		videoPlayer.mozRequestFullScreen();
	} else if (videoPlayer.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
		videoPlayer.webkitRequestFullscreen();
	} else if (videoPlayer.msRequestFullscreen) { /* IE/Edge */
		videoPlayer.msRequestFullscreen();
	}
}

// Add event listener for full screen button click
document.getElementById('videoPlayer').addEventListener('contextmenu', function(event) {
	event.preventDefault(); // Prevent default context menu
	const fullScreenOption = document.createElement('div');
	fullScreenOption.textContent = 'Toggle Full Screen';
	fullScreenOption.classList.add('context-menu-option');
	fullScreenOption.addEventListener('click', toggleFullScreen);

	const contextMenu = document.createElement('div');
	contextMenu.classList.add('context-menu');
	contextMenu.appendChild(fullScreenOption);

	document.body.appendChild(contextMenu);

	contextMenu.style.left = event.clientX + 'px';
	contextMenu.style.top = event.clientY + 'px';

	document.addEventListener('click', function hideContextMenu() {
		document.body.removeChild(contextMenu);
		document.removeEventListener('click', hideContextMenu);
	});
});

// Function to display success alert message
function showSuccessMessage(message) {
	const alertElement = document.createElement('div');
	alertElement.classList.add('alert', 'alert-success');
	alertElement.textContent = message;
	document.getElementById('controls-section').appendChild(alertElement);
}

// Function to display error alert message
function showErrorMessage(message) {
	const alertElement = document.createElement('div');
	alertElement.classList.add('alert', 'alert-danger');
	alertElement.textContent = message;
	document.getElementById('controls-section').appendChild(alertElement);
}
