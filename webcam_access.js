document.addEventListener('DOMContentLoaded', () => {
    const startWebcamButton = document.getElementById('startWebcam');
    const webcamFeed = document.getElementById('webcamFeed');
    const takePictureButton = document.getElementById('takePicture');
    const canvas = document.getElementById('canvas');

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

        //Save the picture to the "apples-and-oranges" folder
        const blob = dataURItoBlob(dataURL);
        const file = new File([blob], 'picture.jpg', {type: 'image/jpeg;'});
        

        try {
            saveAs(file, 'picture.jpg', {autoBom: true});
            console.log('Picture taken and saved!');
        } catch (error) {
            console.log('Error saving picture:', error);
        }
    }

    //Helper function to convert data URL to blob
    function dataURItoBlob(dataURI) {
        const byteString = atob(dataURI.split(',')[1]);
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(buffer);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], {type: 'image/jpeg'});
    }

    // Example: Add a stop button
    // In HTML: <button id="stopWebcam">Stop Webcam</button>
    // In JS:
    const stopWebcamButton = document.getElementById('stopWebcam');
    stopWebcamButton.addEventListener('click', stopWebcamStream);
});