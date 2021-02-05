import React, {Component} from 'react';
import Header from './Header'
import './App.css';
import MainPage from './pages/mainpage'
import AboutPage from './pages/about'
import { BrowserRouter as Router, Route } from "react-router-dom";

class App extends Component{ 
  render(){
      return (
        <body>
          <div id="root">
            <Header />
            <Router>
              <Route exact path="/" component={MainPage} />
              <Route exact path="/about" component={AboutPage} />
            </Router>
          </div>
        </body>
      )
    }
}                 

export default App;