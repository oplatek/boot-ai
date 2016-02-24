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
var Input = ReactBootstrap.Input;

var socket;
var db;

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
  // TODO hide messages http://stackoverflow.com/questions/24171226/react-js-removing-element-from-dom-after-set-amount-of-time
  render:function() {
    var msgAlerts = this.props.msgs.map(function(m) {
      return ( <Alert bsStyle={m.style} key={m.id}>{m.text}</Alert>);
    });
    return (
      <div className="container">
        {msgAlerts}
        <ProgressBar>
          <ProgressBar striped bsStyle="success" now={this.props.stats.correct} key={1} />
          <ProgressBar bsStyle="info" now={this.props.stats.created} key={2} />
          <ProgressBar active bsStyle="danger" now={this.props.stats.errors} key={3} />
        </ProgressBar>
      </div>
      );
  },
});

var HistoryView = React.createClass({
    getDefaultProps() {
        return {
            role: 'COMPULSORY_assistant_or_user',
            msgs:[],
            onSelectedReason: function (action_text) {
                console.log('NotImplemented callback onSelectedReason: ', action_text)
            },
        }
    },
    getInitialState() {
        return { selections: {},}
    },
    handleSelectItem(m) {
        var text = m.target.firstChild.nodeValue
        // FIXME pass the key more sensible way
        var turn_role = m.target.parentElement.childNodes[0].firstChild.nodeValue
        console.log('Selected reason turn_role: ' + turn_role + ' and text ' + text)
        this.props.onSelectedReason(text)
        // make it multiple option
        var {selections} = this.state
        selections[turn_role] = !selections[turn_role]
        this.setState({selections: selections})
    },
    createHistoryItem(m) {
        var turn_role = m.turn + ':' + (this.props.role == m.role ? 'You' : 'System');
        console.log('DEBUG createHistoryItem turn_role ', turn_role, 'props.role', this.props.role, m.role)
        return (<ListGroupItem key={turn_role} active={this.state.selections[turn_role] ? true: false} header={turn_role} onClick={this.handleSelectItem}>{m.text}</ListGroupItem>)
    },
    render() {
        console.log('selections: ', this.state.selections)
        console.log('msgs', this.props.msgs)
        return (
            <div className="actionselectionview">
              <div className="column-header">
                <h3>Select Reasons</h3>
              </div>
              <ListGroup>
                  {this.props.msgs.map(this.createHistoryItem, this)}
              </ListGroup>
            </div>
        )
      },
});

var ActionSelectView;
ActionSelectView = React.createClass({
    getDefaultProps() {
        return {
            actions: [],
            collect_new: true,
            handleNewActionSubmit: function () {
            },
            onSelectedAction: function (action_text) {
                console.log('NotImplemented callback onSelectedAction: ', action_text);
            },
            onNewAction: function (action_text) {
                console.log('NotImplemented callback onNewAction', action_text);
            },
            notifyUser: function (msg) {
                console.log("callback for sending msgs to user: ", m.text, m.style);
            }
        }
    },
    getInitialState() {
        return {
            selections: {},
            new_action: '',
        }
    },
    componentDidMount() {
        console.log('ActionSelect mounted. Actions:', this.props.actions)
    },
    handleSelectItem(m) {
        var text = m.target.firstChild.nodeValue
        console.log('Selected action text: ' + text)
        this.props.onSelectedAction(text);
        // make it single option
        var {selections} = this.state
        selections = {}
        selections[text] = true
        this.setState({selections: selections})
    },
    validationNew(send_msgs = false) {
        let text = this.state.new_action.trim();
        let notify = !this.props.notifyUser;
        if (text.length < 2) {
            if (send_msgs) notify({'text': 'Do not submit empty message!', 'style': 'error'});
            return 'error';
        }
        if (text in this.props.actions) {
            if (send_msgs) notify({
                'text': 'Submit only original action! "' + text + '" is already in actions',
                'style': 'error'
            });
            return 'error';
        }
        return 'success';
    },
    handleNewChange(e) {
        this.setState({new_action: e.target.value});
    },

    handleNewActionSubmit() {
        e.preventDefault();
        var status = validationNew(send_msgs = true);
        var new_text = this.state.new_action.trim();
        this.props.onNewAction(new_text);
    },

    createActionItem(m) {
        return (<ListGroupItem key={m.text} active={this.state.selections[m.text] ? true: false} onClick={this.handleSelectItem}>{m.text}</ListGroupItem>)
    },

    render() {
        console.log('Render(): selection:', this.state.selections)
        return (
            <div clas="actionview">
                <div className="column-header">
                    <h3>Select the Best Action</h3>
                </div>
                <ListGroup>
                    {this.props.actions.map(this.createActionItem, this)}
                </ListGroup>
                {this.props.collect_new ?
                    <Input type="text"
                           value={this.state.new_action}
                           placeholder="If none of actions above don't fit contribute one!"
                           label="Suggested reply"
                           bsStyle={this.validationNew()}
                           groupClassName="group-class"
                           labalClassName="label-class"
                           onChange={this.handleNewChange}
                           onsubmit={this.handleNewActionSubmit}
                    />
                    : <Well>Choose one from the above actions</Well>
                }
            </div>);
    },
});

var DbView = React.createClass({
  getInitialState() {
    return {db_filtered: this._get_default_db()};
  },
  _get_default_db() {
    return [
      {
          "phone": "01223 461661",
          "pricerange": "expensive",
          "addr": "31 newnham road newnham",
          "area": "west",
          "food": "indian",
          "postcode": "not available",
          "name": "india house"
      },
      {
          "addr": "cambridge retail park newmarket road fen ditton",
          "area": "east",
          "food": "italian",
          "phone": "01223 323737",
          "pricerange": "moderate",
          "postcode": "c b 5 8 w r",
          "name": "pizza hut fen ditton"
      }
    ];
  },
  render() {
    return (
      <div className="dbview">
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
    return {
      stats: {correct: 0, created: 0, errors: 0}, 
      msgs:[],
      actions: [],
      new_actions: [],
      action_selected: [],
      history: [],
    };

      // add actions_valid: []
  },
  componentDidMount() {
    console.log('ActionSelect mounted: dialog_id ', this.props.dialog_id, ' role ', this.props.role, 'nick', this.props.nick)
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
    var namespace = '/api';

    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() { 
      socket.emit('join_dialog', {}); 
      console.log('socketio.emit: join_dialog');
    });
    socket.on('redirect', function(msg){ window.location = msg.url; });
    socket.on('messages', this._messagesReceive);
    socket.on('history', this._historyReceive);
    socket.on('actions', this._actionsRecieve);
    socket.on('new_actions', this._new_actionsRecieve);
    socket.on('timeout_select', this._timeout_select);
    socket.on('timeout_turn', this._timeout_turn);
  },

  _messagesReceive(new_msgs) {
    var {msgs} = this.state;
    msgs.push(new_msgs);
    if (msgs.length > 3) {
      msgs.shift()
    };
    this.setState({msgs});
    console.log('Updated msgs:', msgs, 'after new_msgs added', new_msgs);
  },

  _historyReceive(new_history) {
    var {history} = this.state;
    history = new_history;
    this.setState({history});
    if (history.length > 0) {
      console.log('New history received .. last msg', history[history.length-1]);
    } else {
      console.log('Empty history', new_history);
    }
  },

  _actionsRecieve(proposed_actions) {
    var {actions} = this.state;
    actions = proposed_actions;
    this.setState({actions});
    if (actions.length > 0) {
      console.log('Actions[0]', actions[0]);
    } else {
      console.log('No actions were received!', actions);
    }
  },

  _actionsSelected(e) {
    console.log('Action selecte: todo e', e);
  },

  _userSuggestedAction(action_text) {
      console.log('User suggested action ', action_text);
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
      <div>
        <div>
          <MsgAnnouncer msgs={this.state.msgs} stats={this.state.stats} />
        </div>
        <Grid>
          <Row className="show-grid">
            <Col xs={4} md={4}>
              <HistoryView msgs={this.state.history} role={this.props.role} />
            </Col>
            <Col xs={4} md={4}>
              <ActionSelectView actions={this.state.actions} new_actions={this.state.new_actions} selectActionHandler={this._actionsSelected} newActionHandler={this._userSuggestedAction}/>
            </Col>
            <Col xs={4} md={4}>
              <DbView/>
            </Col>
          </Row>
        </Grid>
      </div>
      );


  },
    
});



$(document).ready(function(){
  ReactDOM.render(navbarInstance, document.getElementById('topbar'));

  var dialog_id = document.getElementById('dialog_id').textContent;
  console.log(dialog_id);
  var nick = document.getElementById('author').textContent;
  console.log(nick);
  var role = document.getElementById('role').textContent;
  console.log(role);
  var main = document.getElementById('main');
  ReactDOM.render(<ActionSelect dialog_id={dialog_id} nick={nick} role={role}/>, main);
});
