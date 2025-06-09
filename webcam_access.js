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