import React from 'react';
import PropTypes from 'prop-types';
import SearchComponent from './SearchComponent';
import Results from './Results';
import MySchedule from './MySchedule';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { PostAdd } from '@material-ui/icons';

class Container extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            indexApiurl: "",
            keywordApiurl: "",
            courseApiurl: "",
            results: [],
            myschedule: [],
            showResults: false,
        };
        this.query = this.query.bind(this);
        this.get_schedule = this.get_schedule.bind(this);
        this.handleAddDeleteSchedule = this.handleAddDeleteSchedule.bind(this);
    }

    componentDidMount(){
        this.setState({
            indexApiurl: this.props,
            keywordApiurl: this.props,
            courseApiurl: this.props
        });
        this.get_schedule();
    }

    handleAddDeleteSchedule(courseid, timeid, input){
        const { myschedule } = this.state;
        const{ indexApiurl } = this.props;
        const requestOptions = {
            method: input,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(),
            credentails: 'same-origin',
        };
        let course_time_url = `/api/v1/schedule/user/${courseid}/${timeid}/`;
        fetch(course_time_url, requestOptions)
            .then((response) => {
                console.log(response.status);
                if(response.status==409){
                    alert("You have this class in your schedule!! Select Another Class!");
                }
                if (!response.ok) {
                    throw Error(response.statusText);}
            }).then(() => {
                let url = indexApiurl;
                fetch(url)
                    .then(
                        (response) => response.json(),
                    )
                    .then((data) => {
                        let username = data.username;
                        let schedule_url = `/api/v1/schedule/${username}/`;
                        fetch(schedule_url).then(
                            (response) => response.json(),
                        ).then((user_course_data)=>{
                            if(Object.entries(user_course_data).length==0){
                                this.setState({
                                    myschedule:[],
                                });
                            }
                        })
                    })
                this.get_schedule();
            })
    }

    get_schedule(){
        const{ indexApiurl } = this.props;
        const{ courseApiurl } = this.props;
        let url = indexApiurl;
        const temp_schedule = [];
        fetch(url)
            .then(
                (response) => response.json(),
            )
            .then((data) => {
                let username = data.username;
                let schedule_url = `/api/v1/schedule/${username}/`;
                fetch(schedule_url).then(
                    (response) => response.json(),
                ).then((user_course_data) => {
                    Object.entries(user_course_data).forEach(([k,v]) => {
                        // temp_schedule.push(v);
                        let user_course_dict = {}
                        let courseid = v.courseid;
                        let timeid = v.timeid;
                        // get course name
                        let course_url= `${courseApiurl}${courseid}/`;
                        // console.log(course_url);
                        fetch(course_url).then(
                            (response) => response.json(),
                        )
                        .then((course_info) => {
                            let course_name = course_info.course_name;
                            let course_time_url = `/api/v1/schedule/${courseid}/${timeid}/`;
                            // console.log(course_time_url);
                            fetch(course_time_url).then(
                                (response) => response.json(),
                            )
                            .then((specific_time) => {
                                let endtime = specific_time.endtime;
                                let starttime = specific_time.starttime;
                                let weekday = specific_time.weekday;
                                user_course_dict = {
                                    'endtime': endtime,
                                    'starttime': starttime,
                                    'weekday': weekday,
                                    'courseid': courseid,
                                    'timeid': timeid,
                                    'course_name': course_name,
                                };
                                temp_schedule.push(user_course_dict);
                                if (Object.keys(user_course_data).length === temp_schedule.length){
                                    this.setState({
                                        myschedule: temp_schedule,
                                    });
                                }
                            })
                        })
                    });
                    // console.log(temp_schedule);
                    

                })
            });
    }

    query(input){
        const{ keywordApiurl }= this.props;
        const{ courseApiurl } = this.props;
        this.setState ({
            results: []
        });
        const resHits = {};
        const temp = [];
        let url = keywordApiurl;
        // console.log(url)
        let query = `?q=`;
        query += input.split(' ').join('+');
        url += query;
        // console.log('Url: ', url);
        fetch(url)
            .then(
                (response) => response.json(),
            )
            .then((data)=>{
                const course_list = data.course_list
                if (course_list.length === 0) {
                    this.setState({
                        showResults: true
                    })
                }
                course_list.forEach((element)=>{
                        url= `${courseApiurl}${element}/`;
                        // console.log(url)
                        fetch(url).then(
                            (response) => {
                                if (!response.ok) throw Error(response.statusText);
                                return response.json();}
                        ).then((curData)=> {
                            // console.log(curData)
                            let input = {};
                            input = {
                                'course_id': curData.course_id,
                                'course_name': curData.course_name,
                                'credits': curData.credits,
                                'description': curData.description,
                                'prerequisite': curData.prerequisite,
                            };
                            let courseid = curData.course_id;
                            let schedule_url = `/api/v1/schedule/${courseid}/`
                            let course_time = [];
                            fetch(schedule_url).then(
                                (response) => {
                                    if (!response.ok) throw Error(response.statusText);
                                    return response.json();
                                }
                            ).then((course_time_data) => {
                                Object.entries(course_time_data).forEach(([k,v]) => {
                                    course_time.push(v);
                                    if (Object.keys(course_time_data).length === course_time.length){
                                        input['course_time']=course_time;
                                        resHits[curData.course_id] = input;
                                        if (Object.keys(resHits).length === course_list.length){
                                            course_list.forEach((course)=>{
                                                temp.push(resHits[course]);
                                            });
                                            this.setState({
                                                results: temp,
                                                showResults: true
                                            });
                                        }
                                    }

                                })
                            })
                        })

                    }
                );
            });
    }

    showResults() {
        if (this.state.showResults === true) {
            const paper= {
                padding: '2px',
                textAlign: 'center',
                color: "#2196f3",
            };
            return (
                <Paper style={paper} square={true}>
                    <Results results={this.state.results} submit={this.handleAddDeleteSchedule}/>
                </Paper>
            )
        }
        return (
            <div></div>
        )
    }

    render() {
        const { results } = this.state;
        const { indexApiurl } = this.state;
        const { myschedule } = this.state;
        const { showResults } = this.state;
        const root = {
            flexGrow: 1,
        };
        const paper= {
            padding: '2px',
            textAlign: 'center',
            color: "#2196f3",
        };
        const paper_back ={
            fontSize:'x-large',
            padding: '2px',
            textAlign: 'center',
            color: "white",
            background:"#2196f3",
            height:'50px',
            fontFamily: "Nerko One",
        }
        return (
            <div style={root}>
                <Grid container spacing={3}>
                    <Grid item xs={9}>
                        <Paper style={paper_back}>
                            Search Class by Your Interests
                        </Paper>
                        <Paper style={paper} square={true}>
                        <SearchComponent submit={this.query} />
                        </Paper>
                        {this.showResults()}
                    </Grid>
                    <Grid item xs={3}>
                        <Paper style={paper_back}>
                            My Schedule
                        </Paper>
                        <br></br>
                        <Paper style={paper}>
                            <MySchedule myschedule={myschedule} submit={this.handleAddDeleteSchedule}/>
                        </Paper>
                    </Grid>
                </Grid>
            </div>
            
        )
    }
}

Container.propTypes = {
    indexApiurl: PropTypes.string.isRequired,
    keywordApiurl: PropTypes.string.isRequired,
    courseApiurl: PropTypes.string.isRequired,
  };
  
  export default Container;