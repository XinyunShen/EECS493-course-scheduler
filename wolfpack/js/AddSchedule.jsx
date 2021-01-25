import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

function AddSchedule(props) {
    const { times } = props;
    const { submit } = props;
    const paper= {
        padding: '2px',
        textAlign: 'center',
        color: "#2196f3",
        background:"#f5f5f5",
		fontFamily: "Do Hyeon",
    };
    if (times.length === 2) {
        return(
            <div>
                <Paper style={paper} square={true}>
                    <p>{times[0].weekday}</p>
                    <p>{times[0].starttime} - {times[0].endtime}</p>
                    <Button variant="contained" color="primary" type="submit" onClick={() => {submit(times[0].courseid, times[0].timeid, 'POST'); }}> add</Button>
                    <br></br>
                </Paper>
                <br></br>
                <Paper style={paper} square={true}>
                    <p>{times[1].weekday}</p>
                    <p>{times[1].starttime} - {times[1].endtime}</p>
                    <Button variant="contained" color="primary" type="submit" onClick={() => {submit(times[1].courseid, times[1].timeid, 'POST'); }}> add</Button>
                    <br></br>
                </Paper>
            </div>
         );
    }
    else {
        return(
            <div>
                <Paper style={paper} square={true}>
                    <p>{times[0].weekday}</p>
                    <p>{times[0].starttime} - {times[0].endtime}</p>
                    <Button variant="contained" color="primary" type="submit" onClick={() => {submit(times[0].courseid, times[0].timeid, 'POST'); }}> add</Button>
                    <br></br>
                </Paper>
            </div>
         );
    }
}

AddSchedule.propTypes = {
    times: PropTypes.arrayOf(
        PropTypes.shape({
            courseid: PropTypes.number,
            timeid: PropTypes.number,
            endtime: PropTypes.string,
            starttime: PropTypes.string,
            weekday: PropTypes.string,

        })
    ).isRequired,
    submit: PropTypes.func.isRequired,
};

export default AddSchedule;