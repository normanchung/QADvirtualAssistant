import React from 'react';
import logo from './icon.JPG';
import './App.css';

function App() {
  return (
    <body>
    <div id="root">
      <div class="View"> 
        <h1 class="Banner">22222222</h1>
        <img src={logo} className="App-logo" />
      </div>
      <div class="View">
        <div class = "search">
        <input type="text" placeholder="Search..."></input>
        </div>
        <div class="NavButtons"><a href="http://localhost:3000">
            <div class="NavButton">Action</div></a></div>
      </div>
    </div>
  </body>
  );
}

export default App;