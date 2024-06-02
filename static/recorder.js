const recordButton = document.getElementById('record-btn');



async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
  
    const audioChunks = [];

    function changeButton() {
      recordButton.style.backgroundColor='red'; recordButton.textContent = 'Stopped'; }


    recordButton.addEventListener('click', () => {mediaRecorder.stop(); changeButton()});

    function waitingForResponse() {  
      let wait = document.getElementById('error')
      if (wait.textContent= ' ' ) {
        wait.textContent = 'Waiting for Sam...'
    
      } else {
        wait.textContent = 'none'
      }
    }
    
    if (recordButton.textContent == 'Stopped') {
      waitingForResponse()
    }
    
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
          let msg = document.getElementById('error')
          msg.textContent = 'Audio uploaded successfully!'
          console.log('Audio uploaded successfully!');
          window.location.reload();
        } else {
          let msg = document.getElementById('error')
          msg.textContent = `${response.statusText}`
          console.error('Error uploading audio:', response.statusText);
        }
      } catch (error) {
        let msg = document.getElementById('error')
        msg.textContent = `${error}`
        console.error('Error uploading audio:', error);
      } finally {
        recordButton.textContent = 'Record  ';
        recordButton.disabled = false;
        stream.getTracks().forEach(track => track.stop());
      }
    };

    mediaRecorder.start();

  } catch (error) {
    let msg = document.getElementById('error')
    msg.textContent = `${error}`
    console.error('Error accessing microphone:', error);
  }
}


recordButton.addEventListener('click', startRecording)

  