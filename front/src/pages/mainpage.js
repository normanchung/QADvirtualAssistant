import React, {useRef, useEffect} from 'react';
import {Widget} from 'rasa-webchat';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMicrophone } from '@fortawesome/free-solid-svg-icons'
import Granim from 'react-granim'

var listening = false;

function MyComponent() {
    const webchatRef = useRef(null);
    const { transcript, interimTranscript, finalTranscript, resetTranscript} = useSpeechRecognition()

    useEffect(() => {
      if (finalTranscript !== '') {
        callback();
        resetTranscript();
        stopListening();
        listening = false;
      }}
    );

    function handleListen(){
      if (!listening){
        listening = true;
        SpeechRecognition.startListening();
        isListening();
        setTimeout(() => { 
          if (finalTranscript === ''){
            SpeechRecognition.stopListening();
            stopListening();
            listening = false;
          }
        }, 5000);
      }
    }

    function isListening(){
      Array.from(document.querySelectorAll('.speech-button')).map(function(button) {
                 button.style.color="#6495ED";
                 button.style.border="1px solid white";
      })
    }

    function stopListening(){
      Array.from(document.querySelectorAll('.speech-button')).map(function(button) {
        button.style.color="white";
        button.style.border="1px solid grey";
      })
    }
    
    function callback() {
        if (webchatRef.current && webchatRef.current.sendMessage) {
          webchatRef.current.sendMessage(finalTranscript, finalTranscript);
        }
    }
    
    return (<div class = "chatroom">
      <Widget 
        initPayload={""}
        socketUrl={"http://localhost:5005"}
        socketPath={"/socket.io/"}
        inputTextFieldHint={"Enter a valid command"}
        customData={{"language": "en"}} // arbitrary custom data. Stay minimal as this will be added to the socket
        title={"QAD Virtual Assistant"}
        showFullScreenButton={"true"}
        embedded={"true"}
        hideWhenNotConnected = {"false"}
        params={{"storage": "session"}}
      ref={webchatRef}/>
      <button class = "speech-button" onClick={handleListen}><FontAwesomeIcon icon={faMicrophone} /></button>
    </div>)
}

const MainPage = () => {
    return(
        <div class="View">
          {/* <div> */}
          {/* <img src = "bg.png" class = "background"></img> */}
          <div class = "granim">
            <Granim id="granim" height = "10"></Granim>
          </div>
          {/* </div> */}
          <h1 class = "command">
              How can I help?
          </h1>
          <div>
              <MyComponent />
          </div>
        </div>
    );
};
export default MainPage;
