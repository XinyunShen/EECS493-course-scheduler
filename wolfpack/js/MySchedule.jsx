import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

function MySchedule(props){
    const { myschedule } = props;
    const { submit } = props;
    const root = {
        flexGrow: 1,
    };
    const paper= {
        padding: '2px',
        textAlign: 'center',
        color: "#2196f3",
    };
    const time_info={
        color:'#bdbdbd',
        padding:'2px',
        margin:'0px',
    }
    const course_info={
        color:'#1976d2',
        padding:'2px',
        margin:'0px',
    }
    return (
        myschedule.map((schedule) => (
            <div key={schedule.timeid}>
                <p style={course_info}>{schedule.courseid} {schedule.course_name}</p>
                <p style={time_info}>{schedule.weekday}</p>
                <p style={time_info}>{schedule.starttime} -{schedule.endtime}</p>
                <Button variant="contained" color="primary" type="submit" onClick={() => {submit(schedule.courseid, schedule.timeid, 'DELETE'); }}> remove</Button>
                <br></br><br></br>
            </div>
        ))
    )
};

MySchedule.propTypes = {
    myschedule : PropTypes.array.isRequired,
    submit: PropTypes.func.isRequired,
}

export default MySchedule