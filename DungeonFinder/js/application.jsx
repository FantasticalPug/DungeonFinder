import React from 'react';
import PropTypes from 'prop-types';

class Application extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            gameid: '',
            questions: [],
        };
    }

    componentDidMount() {
        const {
            gameid,
        } = this.props;
        this.setState({
            gameid,
        });
        let url = `/api/v1/applications/questions/?gameid=${this.props.gameid}`
        let method = 'GET'
        fetch(url, {
            method,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            let questions = []
            for (let i = 0; i < data.questions.length; i += 1) {
                let key = `question-${questions.length}`
                let num = questions.length + 1
                questions.push(
                    <p key={key} className="question">
                        Question {num}: {data.questions[i]['question']}
                    </p>
                );
            }
            this.setState({
                questions,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        this.add = this.add.bind(this);
    }

    add(event) {
        let question = document.getElementById('new-question').value
        if (question.length === 0) {
            return;
        }
        let url = `/api/v1/applications/add/?gameid=${this.state.gameid}&question=${question}`
        let method = 'POST'
        fetch(url, {
            method,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            let questions = []
            for (let i = 0; i < data.questions.length; i += 1) {
                let key = `question-${questions.length}`
                let num = questions.length + 1
                questions.push(
                    <p key={key} className="question">
                        Question {num}: {data.questions[i]['question']}
                    </p>
                );
            }
            this.setState({
                questions,
            });
            document.getElementById('new-question').value = ""
        })
        .catch((error) => {
            console.log(error);
        });
        event.preventDefault();
    }

    render() {
        const {
            questions,
            gameid,
        } = this.state;
        let url = `/games/${gameid}/`
        return (
            <span>
                {questions}
                <input className="question-field" id="new-question" placeholder="Add a Question"/>
                <button className="btn btn-primary" onClick={this.add}>Add Question</button>
                <a href={url} className="btn btn-primary">Create Application</a>
            </span>
        );
    }

}

Application.propTypes = {
    gameid: PropTypes.string.isRequired,
};

export default Application;
