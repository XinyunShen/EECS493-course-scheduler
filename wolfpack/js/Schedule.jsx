import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';
import '../static/css/reactSchedule.css'
import PropTypes from 'prop-types';
import AddSchedule from './AddSchedule';


class Schedule extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            data: [],
            to_day: {
                'Monday': 12,
                'Tuesday': 13,
                'Wednesday': 14,
                'Thursday': 15,
                'Friday': 16
            },
            finish_fetch: false,
            colors: [
                '#EE6345',
                '#F09B3D',
                '#ECD235',
                '#9ADC32',
                '#32DC90',
                '#289CCD',
                '#5A63D3',
                '#9667C4',
                '#DD46E4',
                '#E44695',
                '#E44654',
                '#B8EC61',
                '#95D0BE',
                '#CE95D0'
            ]
        };
        this.get_user_schedule = this.get_user_schedule.bind(this);
        this.submit = this.props.submit;
    }

    componentDidMount(){
        this.setState({
            username: this.props,
        });
        this.get_user_schedule();
    }


    get_user_schedule(){
        const {username} = this.props;
        const {to_day} = this.state;
        fetch(`/api/v1/schedule/${username}/complete`)
        .then(
            (response) => response.json(),
        )
        .then((data) => {
            for (var key in data) {
                for(var course in data[key]){
                    var starttime = data[key][course]['starttime'].split(":");
                    var endtime = data[key][course]['endtime'].split(":");
                    var temp = {
                        Id: data[key][course]['courseid'],
                        Subject: data[key][course]['coursename'],
                        StartTime: new Date(2018, 1, to_day[key], starttime[0], starttime[1]),
                        EndTime: new Date(2018, 1, to_day[key], endtime[0], endtime[1]),
                        IsAllDay: false,
                        Status: 'Completed',
                        Priority: 'High',
                        CategoryColor: this.state.colors[data[key][course]['timeid'] % 14],
                        Description: data[key][course]['description'],
                        Timeid: data[key][course]['timeid']
                    }
                    this.state.data.push(temp);
                }
            }
            this.setState({
                finish_fetch: true
            })
        });
    }

    onPopupOpen(args) {
        console.log("HERE")
        if ((!args.target.classList.contains('e-appointment') && (args.type === 'QuickInfo')) || (args.type === 'Editor')) {
            args.cancel = true;
        }
        const btn = document.createElement("BUTTON");
        btn.innerHTML = "Add to Schedule";
        const submit = this.props.submit;
        btn.onclick = function(){
            submit(args.data.Id, args.data.Timeid, 'POST');
        };
        args.element.appendChild(btn);
    }

    onEventRendered(args) {
        args.element.style.backgroundColor = args.data.CategoryColor;
    }

    render() {
        if (this.state.finish_fetch){
            return (
                <div 
                    style={{
                        borderWidth: 6, 
                        borderColor: "lightgray", 
                        borderStyle: "solid",
                        paddingLeft: 15,
                        paddingRight: 15,
                        paddingTop: 5,
                        paddingBottom: 5,
                        margin: 20
                    }}
                >
                    <a class="navbar-brand" href={`/u/${this.props.username}/`}>{this.props.username}</a>
                    <ScheduleComponent 
                        height='600px'
                        startHour='08:00' endHour='18:30'
                        showHeaderBar = {false} 
                        showWeekend={false} selectedDate={new Date(2018, 1, 15)} 
                        eventSettings={{ 
                            dataSource: this.state.data,
                            fields: {
                                id: 'Id',
                                subject: { name: 'Subject' },
                                isAllDay: { name: 'IsAllDay' },
                                startTime: { name: 'StartTime' },
                                endTime: { name: 'EndTime' },
                                CategoryColor: 'Color'
                            }}}
                        popupOpen={this.onPopupOpen.bind(this)}
                        eventRendered={this.onEventRendered.bind(this)}
                    >
                    <Inject services={[Day, Week, WorkWeek, Month, Agenda]}/>
                    </ScheduleComponent>
                </div>
            )
        }
        return <div>Loading...</div>
    }
}

Schedule.propTypes = {
    username: PropTypes.string.isRequired,
    submit: PropTypes.func.isRequired
};

export default Schedule;