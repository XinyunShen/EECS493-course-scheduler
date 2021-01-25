import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import AddSchedule from './AddSchedule';

function Results(props) {
	const { results } = props;
	const { submit } = props;
	console.log("submit in results")
	// console.log(submit);
    const root = {
      flexGrow: 1,
    };
    const paper= {
        padding: '2px',
        textAlign: 'center',
		color: "#2196f3",
		fontFamily: "Do Hyeon",
	};
	const paper_title={
		padding: '2px',
        textAlign: 'center',
		color: "white",
		background: '#2196f3',
		fontFamily: "Do Hyeon",
	};
	const space ={
		height: '40px',
		padding: '20px',
	};
	const content={
		color:'black',
		fontFamily:'Roboto',
	}
	if (results.length === 0) {
      return (<div style={root}>no results</div>);
    }
    return (
      results.map((result) => (
        <div key={result.course_id} style={root}>
			<Grid container spacing={3}>
				<Grid item xs={9}>
					<Paper style={paper_title} square={true}>
					{result.course_id} {result.course_name}
					</Paper>
					<Paper style={paper} square={true}>
						<Grid container spacing={3}>
							<Grid item xs={3}>
								CREDITS
							</Grid>
							<Grid item xs={9} style={content}>
								{result.credits}
							</Grid>
						</Grid>
					</Paper>
					<Paper style={paper} square={true}>
						<Grid container spacing={3}>
							<Grid item xs={3}>
								DESCTIPTION
							</Grid>
							<Grid item xs={9} style={content}>
								{result.description}
							</Grid>
						</Grid>
					</Paper>
					<Paper style={paper} square={true}>
						<Grid container spacing={3}>
							<Grid item xs={3}>
								PREREQUISITE
							</Grid>
							<Grid item xs={9} style={content}>
								{result.prerequisite}
							</Grid>
						</Grid>
					</Paper>
					<Paper style={paper} square={true}>
						<br></br>
					</Paper>
				</Grid>	
				<Grid item xs={3}>
					<AddSchedule times={result.course_time} submit={submit}/>
				</Grid>
				<div style={space}></div>
			</Grid>
        </div>
      ))
    );
  }
  
  Results.propTypes = {
    results: PropTypes.arrayOf(
        PropTypes.shape({
            course_id: PropTypes.number,
            course_name: PropTypes.string,
            credits: PropTypes.number,
            description: PropTypes.string,
            prerequisite: PropTypes.string,
        })
	).isRequired,
	submit: PropTypes.func.isRequired,
  };
  
  export default Results;
  