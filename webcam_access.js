document.addEventListener('DOMContentLoaded', () => {
    const startWebcamButton = document.getElementById('startWebcam');
    const webcamFeed = document.getElementById('webcamFeed');
    const takePictureButton = document.getElementById('takePicture');
    const canvas = document.getElementById('canvas');
    canvas.width = 640;
    canvas.height = 480;

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

    takePictureButton.addEventListener('click', () => {
        takePicture(webcamFeed, canvas);
    });

    // Function to stop the webcam stream
    function stopWebcamStream() {
        if (webcamFeed.srcObject) {
            const tracks = webcamFeed.srcObject.getTracks();
            tracks.forEach(track => track.stop()); // Stop each track
            webcamFeed.srcObject = null; // Clear the srcObject
        }
    }

    // Function to take a picture
    function takePicture(video, canvas) {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL();
        console.log(dataURL); //Log the picture data URL
        console.log('Picture taken:', dataURL);
    }

    // Example: Add a stop button
    // In HTML: <button id="stopWebcam">Stop Webcam</button>
    // In JS:
    const stopWebcamButton = document.getElementById('stopWebcam');
    stopWebcamButton.addEventListener('click', stopWebcamStream);
});