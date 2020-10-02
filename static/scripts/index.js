import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Search from './Search';

ReactDOM.render(<App search={ document.getElementById('root').getAttribute('search') } />, document.getElementById('root'));


