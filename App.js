import React, { useState, useEffect } from 'react';

const SpeechToText = () => {
  const [transcription, setTranscription] = useState('(Not listening)');
  let recognition = null;
  let lastRecognizedIndex = 0;

  useEffect(() => {
    // Check for the existence of the Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      // Event handler when the recognition service returns a result
      recognition.onresult = (event) => {
        let interimTranscript = '';

        for (let i = lastRecognizedIndex; i < event.results.length; ++i) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            setTranscription((prevTranscription) => prevTranscription + transcript + ' ');
          } else {
            interimTranscript += transcript;
          }
        }

        // Update interim transcript more frequently
        setTranscription((prevTranscription) => prevTranscription + interimTranscript);
        lastRecognizedIndex = event.results.length;
      };

      // Start listening
      recognition.start();
    } else {
      console.error('Web Speech API is not supported in this browser.');
    }

    // Cleanup recognition when the component unmounts
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);

  return (
    <div>
      <h1>Speech-to-Text with React</h1>
      <p>{transcription}</p>
    </div>
  );
};

export default SpeechToText;
