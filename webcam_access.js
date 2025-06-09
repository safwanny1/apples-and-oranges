document.addEventListener('DOMContentLoaded', () => {
    const startWebcamButton = document.getElementById('startWebcam');
    const webcamFeed = document.getElementById('webcamFeed');

    startWebcamButton.addEventListener('click', async () => {
        try {
            // Request access to the video stream (webcam)
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });

            // Attach the stream to the video element
            webcamFeed.srcObject = stream;

            // Play the video
            webcamFeed.onloadedmetadata = () => {
                webcamFeed.play();
            };

        } catch (err) {
            // Handle errors (e.g., user denied permission, no webcam found)
            console.error('Error accessing webcam:', err);
            alert(`Error accessing webcam: ${err.name} - ${err.message}`);
        }
    });
});
// Function to stop the webcam stream
function stopWebcamStream() {
    if (webcamFeed.srcObject) {
        const tracks = webcamFeed.srcObject.getTracks();
        tracks.forEach(track => track.stop()); // Stop each track
        webcamFeed.srcObject = null; // Clear the srcObject
    }
}

// Example: Add a stop button
// In HTML: <button id="stopWebcam">Stop Webcam</button>
// In JS:
const stopWebcamButton = document.getElementById('stopWebcam');
stopWebcamButton.addEventListener('click', stopWebcamStream);