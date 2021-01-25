import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

class SearchComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          input: '',
        };
        this.handleTextChange = this.handleTextChange.bind(this);
    }
    handleTextChange(event) {
        this.setState({ input: event.target.value });
    }
    render(){
        const { input } = this.state;
        const root = {
            flexGrow: 1,
        };
        const paper= {
            padding: '2px',
            textAlign: 'center',
            color: "#2196f3",
        };
        const space={
            height: '20px',
        }
        return(
            <div style={root}>
                <Paper style={paper} square={true}>
                    <br></br>
                </Paper>
                <Paper style={paper} square={true}>
                    keyword:&nbsp;
                    <input
                type="text"
                name="text"
                value={input}
                onChange={this.handleTextChange}
                />
                </Paper>
                <Paper style={paper} square={true}>
                    <br></br>
                </Paper>
                <Paper style={paper} square={true}>
                    <Button variant="contained" color="primary" type="submit" onClick={() => { const { submit } = this.props; submit(input); }}> submit</Button>
                    <div style={space}></div>
                </Paper>
                        
                
            </div>
        )

    }
    
}

SearchComponent.propTypes = {
    submit: PropTypes.func.isRequired,
};
  
  export default SearchComponent;