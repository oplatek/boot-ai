// TODO create components which can dynamically display the json data.


var Nav = ReactBootstrap.Nav;
var NavItem = ReactBootstrap.NavItem;
var Navbar = ReactBootstrap.Navbar;
var NavDropdown = ReactBootstrap.NavDropdown;
var MenuItem = ReactBootstrap.MenuItem;
var Table = ReactBootstrap.Table;
var ListGroup = ReactBootstrap.ListGroup;
var ListGroupItem = ReactBootstrap.ListGroupItem;
var ListGroupItemText = ReactBootstrap.ListGroupItemText;
var ProgressBar = ReactBootstrap.ProgressBar;
var Alert = ReactBootstrap.Alert;
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;

var socket;
var db;

// TODO load the data
var history = [
    {id:0, value: "Good morning. How may I help you?", reason: false, author: "id-you"},
    {id:1, value: "I would like to know what is the nearest Sweet shop near Fisherman's wharf?", reason: false, author: "id-other-1"},
    {id:2, value: "Give me few seconds. I will look it up.", reason: false, author: "id-you"},
    {id:3, value: "Sure", reason: false, author: "id-other-2"},
    {id:4, value: "Select new action from the options and mark at least one from the actions above as reasons why you have chosen that action", reason: false, author: "id-you"}
    ];

// TODO load the data
var actions = [ {id:1, value: "Give me a bit more time...", selected: false, author: "crowd-1"},
    {id:2, value: "I am sorry, I do not have enough information to answer.", selected: false, author: "crowd-1"},
    {id:3, value: "I found many options would you like to hear few examples?", selected: false, author: "crowd-1"},
    {id:4, value: "Great! I love sweets!", selected: false, author: "crowd-1"}
    ];


const navbarInstance = (
  <Navbar inverse fixed-top>
    <Navbar.Header>
      <Navbar.Brand>
        <a href="#">Boot-AI</a>
      </Navbar.Brand>
    </Navbar.Header>
    <Nav>
      <NavItem eventKey={1} href="#" active>Return to Crowdflower</NavItem>
      <NavDropdown eventKey={3} title="Help" id="basic-nav-dropdown">
        <MenuItem eventKey={3.1}>Point Scoring</MenuItem>
        <MenuItem eventKey={3.2}>Recommended Strategy</MenuItem>
        <MenuItem eventKey={3.3}>Task Description</MenuItem>
        <MenuItem divider />
        <MenuItem eventKey={3.4}>Top Scores</MenuItem>
        <MenuItem eventKey={3.5}>See dialogs examples</MenuItem>
      </NavDropdown>
    </Nav>
  </Navbar>
);


var MsgAnnouncer = React.createClass({
  getInitialState: function() {
    return {correct: 0, created: 0, errors: 0, msgs:[]};
    // return {correct: 35, created: 20, errors: 10, msgs: [{style: "success", id: "1", text: "Great! You and two other people agreed to choose action 3."}]};
  },

  // replace with socketio
  // loadStatsFromServer: function() {
  //   $.ajax({
  //     url: this.props.url  + '/api/stats/dialog/' + this.props.dialog_id + '/user/' + this.props.user_id + '/turn/' + this.props.turn,
  //     dataType: 'json',
  //     cache: false,
  //     success: function(stats) {
  //       this.setState({correct: stats["correct"]});
  //       this.setState({created: stats["created"]});
  //       this.setState({errors: stats["errors"]});
  //     }.bind(this),
  //     error: function(xhr, status, err) {
  //       console.error(this.props.url, status, err.toString());
  //     }.bind(this)
  //   });
  // },
  // loadMsgsFromServer: function() {
  //   $.ajax({
  //     url: this.props.url  + '/api/messages/dialog/' + this.props.dialog_id + '/user/' + this.props.user_id + '/turn/' + this.props.turn,
  //     dataType: 'json',
  //     cache: false,
  //     success: function(messages) {
  //       this.setState({msgs: messages});
  //     }.bind(this),
  //     error: function(xhr, status, err) {
  //       console.error(this.props.url, status, err.toString());
  //     }.bind(this)
  //   });
  // },

  componentDidMount: function() {
    // FIXME callbacks from parent
    // this.loadMsgsFromServer();
    // setInterval(this.loadMsgsFromServer, this.props.pollInterval);
  },
  render:function() {
    var msgAlerts = this.state.msgs.map(function(m) {
      return ( <Alert bsStyle={m.style} key={m.id}>{m.text}</Alert>);
    });

    return (
      <div>
        <ProgressBar>
          <ProgressBar striped bsStyle="success" now={this.state.correct} key={1} />
          <ProgressBar bsStyle="info" now={this.state.created} key={2} />
          <ProgressBar active bsStyle="danger" now={this.state.errors} key={3} />
        </ProgressBar>
        {msgAlerts}
      </div>
    );
  },
});

var HistoryView = React.createClass({
  render() {
      return (
        <div class="actionselectionview">
          <div className="column-header">
            <h3>Select Reasons</h3>
          </div>
          <ListGroup>
            <ListGroupItem href="#" header="Assistant" text="" active>
              Todo generate dynamicly from the json
            </ListGroupItem>
            <ListGroupItem href="#" header="You">todo 2</ListGroupItem>
            <ListGroupItem header="Assistant" disabled active>Select new action from the options and mark at least one from the actions above as reasons why you have chosen that action  3</ListGroupItem>
          </ListGroup>
        </div>);
  },
});


var ActionSelectView = React.createClass({
  render() {
    return (
      <div clas="historyview">
        <div className="column-header">
          <h3>Select the Best Action</h3>
        </div>
        <ListGroup>
          <ListGroupItem href="#" active>Todo generate dynamicly from the json</ListGroupItem>
          <ListGroupItem href="#">todo 2</ListGroupItem>
          <ListGroupItem href="#" disabled>todo - others disabled  3</ListGroupItem>
        </ListGroup>
        <div className="form-group">
            <label for="new_action">Your proposal if above actions are not applicable:</label>
              <textarea className="form-control" rows="5" id="new_action">You can use # for database entities and e.g. @user1 for selecting reasons"</textarea>
        </div>
      </div>);
  },
});

var DbView = React.createClass({
  render() {
    return (
      <div class="dbview">
        <div className="column-header">
          <h3>Find and Mark Info</h3>
        </div>
        <Table hover>
            <thead>
              <tr>
                <th>#</th>
                <th>Restaurant</th>
                <th>Price Range</th>
                <th>Address</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Ask</td>
                <td>Medium</td>
                <td>12 Bridge St, Cambridge</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Pizza place</td>
                <td>Cheap</td>
                <td>3 Churchill St, Cambridge</td>
              </tr>
              <tr>
                <td>3</td>
                <td>Kebab place</td>
                <td>Cheap</td>
                <td>Queen Mary Sq, Cambridge</td>
              </tr>
            </tbody>
          </Table>
        </div>);
  },
});

var ActionSelect = React.createClass({
  getInitialState() {
    // FIXME db is loaded with AJAX as top level variable
    return {messages:[], history: {}, actions: {}};
  },
  componentDidMount() { 

    db = {"FIXME": "FIXME"};
    // $.ajax({
    //   url: '/api/dialog/db/dstc2',
    //   dataType: 'json',
    //   cache: true,
    //   success: function(db_received) {
    //     db = db_received;
    //   },
    //   error: function(xhr, status, err) {
    //     console.error(status, err.toString());
    //   }
    // });

    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() { socket.emit('joined_dialog', {}); });
    socket.on('messages', this._messagesReceive);
    socket.on('history', this._historyReceive);
    socket.on('actions', this._actionsRecieve);
    socket.on('new_actions', this._new_actionsRecieve);
    socket.on('timeout_select', this._timeout_select);
    socket.on('timeout_turn', this._timeout_turn);
  },

  _messagesReceive(msgs) {
    console.log('receive msg', msgs);
    // TODO
  },

  _historyReceive(msgs) {
    console.log('receive history', msgs);
    // TODO
  },

  _actionsReceive(msgs) {
    console.log('receive actions', msgs);
    // TODO
  },

  _new_actionsReceive(msgs) {
    console.log('receive actions', msgs);
    // TODO
  },

  _timeout_select(msgs) {
    console.log('timeout select');
  },

  _timeout_turn(msgs) {
    console.log('timeout turn');
  },

  render() {
    return (
      <Grid>
        <Row className="show-grid">
          <Col xs={4} md={4}>
            <HistoryView/>
          </Col>
          <Col xs={4} md={4}>
            <ActionSelectView/>
          </Col>
          <Col xs={4} md={4}>
            <DbView/>
          </Col>
        </Row>
      </Grid>);

  },
    
});



$(document).ready(function(){
  ReactDOM.render(navbarInstance, document.getElementById('topbar'));
  // NOT SURE IF TURN IS property or state
  ReactDOM.render(<MsgAnnouncer url="/api/dialog" dialog_id={6} pollInterval={2000} user_id={1} turn={8}/>, document.getElementById('messages'));

  var dialog_id = document.getElementById('dialog_id').textContent;
  console.log(dialog_id);
  var nick = document.getElementById('author').textContent;
  console.log(nick);
  var role = document.getElementById('role').textContent;
  console.log(role);
  var main = document.getElementById('main');
  ReactDOM.render(<ActionSelect dialog_id={dialog_id} nick={nick} role={role}/>, main);
});