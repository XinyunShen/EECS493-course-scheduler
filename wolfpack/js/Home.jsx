import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

function Home(props){
    return (
        <div style={{textAlign: 'center', paddingTop: '15px'}}>
            <h1>Wolverine Scheduler</h1>
            <br></br>
            <img src={"../static/logo.png"}/>
        </div>
    )
};

// MySchedule.propTypes = {
//     myschedule : PropTypes.array.isRequired,
//     submit: PropTypes.func.isRequired,
// }

export default Home