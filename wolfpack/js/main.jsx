import React from 'react';
import ReactDOM from 'react-dom';
import Container from './Container';
import Feed from './Feed';
import Home from './Home';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Switch
} from 'react-router-dom'

// This method is only called once
// const element = <h1>Hello</h1>;
// ReactDOM.render(element, document.getElementById('reactEntry'));

// class App extends Component {
//   render(){
//     return (
      
//     )
//   }
// }

ReactDOM.render(
  // Insert the likes component into the DOM
  <Router>
    <ul className="nav nav-tabs">
      <li class="nav-item">
        <Link to="/class" className="nav-link active" data-toggle="tab">Add Classes</Link>
      </li>
      <li className="nav-item">
        <Link to="/feed" className="nav-link active" data-toggle="tab">My Friends</Link>
      </li>
    </ul>   
    <Switch>
      <Route path='/class' render={(props) => (
        <Container indexApiurl= "/api/v1/" keywordApiurl="/api/v1/hits/" courseApiurl="/api/v1/courses/"></Container>
      )}/>
      <Route path='/feed' render={(props) => (
        <Feed indexApiurl= "/api/v1/" courseApiurl="/api/v1/courses/"></Feed>
      )}/>
      <Route path='/' render={(props) => (
        <Home></Home>
      )}/>
    </Switch>  
  </Router>,
  document.getElementById('reactEntry'),  
);