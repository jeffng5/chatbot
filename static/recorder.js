const recordButton = document.getElementById('record-btn');



async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    console.log(mediaRecorder)
    const audioChunks = [];

    recordButton.textContent = 'Record';
    recordButton.addEventListener('click', () => {mediaRecorder.stop()});
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob);

      try {
        const response = await fetch('/conversation', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          console.log('Audio uploaded successfully!');
          window.location.reload();
        } else {
          console.error('Error uploading audio:', response.statusText);
        }
      } catch (error) {
        console.error('Error uploading audio:', error);
      } finally {
        recordButton.textContent = 'Record';
        recordButton.disabled = false;
        stream.getTracks().forEach(track => track.stop());
      }
    };

    mediaRecorder.start();

  } catch (error) {
    console.error('Error accessing microphone:', error);
  }
}

recordButton.addEventListener('click', startRecording);
  