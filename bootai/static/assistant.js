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
        <MenuItem eventKey={3.5}>See dialogues examples</MenuItem>
      </NavDropdown>
    </Nav>
  </Navbar>
);


var MsgAnnouncer = React.createClass({
  getInitialState: function() {
    return {correct: 0, created: 0, errors: 0, msgs:[]};
    // return {correct: 35, created: 20, errors: 10, msgs: [{style: "success", id: "1", text: "Great! You and two other people agreed to choose action 3."}]};
  },
  loadStatsFromServer: function() {
    $.ajax({
      url: this.props.url  + '?' + 'dialogue_id=' + this.props.dialogue_id + '&' + 'stats=yes' + '&' + 'user_id=' + this.props.user_id,
      dataType: 'json',
      cache: false,
      success: function(stats) {
        this.setState({correct: stats["correct"]});
        this.setState({created: stats["created"]});
        this.setState({errors: stats["errors"]});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loadMsgsFromServer: function() {
    $.ajax({
      url: this.props.url + '?' +  'dialogue_id=' + this.props.dialogue_id + '&' + 'msgs=yes' + '&' + 'user_id=' + this.props.user_id,
      dataType: 'json',
      cache: false,
      success: function(messages) {
        this.setState({msgs: messages});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadMsgsFromServer();
    setInterval(this.loadMsgsFromServer, this.props.pollInterval);
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


const gridInstance = (
  <Grid>

    <Row className="show-grid">
      <Col xs={4} md={4}>
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
      </Col>
      <Col xs={4} md={4}>
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
      </Col>
      <Col xs={4} md={4}>
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
      </Col>
    </Row>

  </Grid>
);



ReactDOM.render(navbarInstance, document.getElementById('todo1'));
ReactDOM.render(<MsgAnnouncer url="/api/dialogue" dialogue_id={6} pollInterval={2000} user_id={1}/>, document.getElementById('todo2'));
ReactDOM.render(gridInstance, document.getElementById('todo4'));
