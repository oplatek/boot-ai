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

// TODO show help locally
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


var MsgAnnouncer;
MsgAnnouncer= React.createClass({
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
            active: true,
            role: 'COMPULSORY_assistant_or_user',
            msgs:[],
            onReasonsChanged: function(selection_dict) {
                console.log('Register your callback to: ', action_text)

            },
        }
    },
    getInitialState() {
        return {
            selections: {},
        }
    },
    handleSelectItem(m) {
        if(this.props.active) {
            var text = m.target.firstChild.nodeValue
            // FIXME pass the key more sensible way
            var turn_role = m.target.parentElement.childNodes[0].firstChild.nodeValue
            console.log('Selected reason turn_role: ' + turn_role + ' and text ' + text)
            // make it multiple option
            var {selections} = this.state
            selections[turn_role] = !selections[turn_role]
            this.setState({selections: selections})
            this.props.onReasonsChanged(this.state.selections)
        } else {
            // TODO make it visually understandable
            console.log('Cannot change the item HistoryView changes are disabled')
        }
    },
    createHistoryItem(m) {
        var turn_role = m.turn + ':' + (this.props.role == m.role ? 'You' : 'System');
        //console.log('DEBUG createHistoryItem turn_role ', turn_role, 'props.role', this.props.role, m.role)
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
            active: true,
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
            notifyUser: function (msgs) {
                console.log("callback for sending msgs to user: ", m.text, m.style);
            }
        }
    },
    getInitialState() {
        return {
            selections: {},
            suggested_action: '',
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
        let text = this.state.suggested_action.trim();
        let notify = this.props.notifyUser;
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
        this.setState({suggested_action: e.target.value});
    },
    handleKeyPress(target) {
        if(target.charCode==13) {
            var status = this.validationNew(true);
            if (status == 'success') {
                var new_text = this.state.suggested_action.trim();
                console.log('Suggested action validated', new_text);
                this.props.onNewAction(new_text);
            }
        }
    },
    createActionItem(m) {
        return (<ListGroupItem key={m.text} active={this.state.selections[m.text] ? true: false} onClick={this.handleSelectItem}>{m.text}</ListGroupItem>)
    },
    render() {
        //console.log('Render(): selection:', this.state.selections)
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
                           value={this.state.suggested_action}
                           placeholder="If none of actions above don't fit contribute one!"
                           label="Suggest action"
                           bsStyle={this.validationNew()}
                           groupClassName="group-class"
                           labalClassName="label-class"
                           onChange={this.handleNewChange}
                           onKeyPress={this.handleKeyPress}
                    />
                    : <Well>Choose one from the above actions</Well>
                }
            </div>);
    },
});


var DbView;
DbView = React.createClass({
    getInitialState() {
        return {db_filtered: this._get_default_db()};
    },
    getDefaultProps() {
        return {
            active: true,
        }
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


var ActionSelect;
ActionSelect= React.createClass({
  getInitialState() {
    return {
        active: true,
        stats: {correct: 0, created: 0, errors: 0},
        msgs:[],
        actions: [],
        history: [],
        turn_reasons_from_history: [],
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
    socket.on('add_actions', this._additional_actionReceive);
    socket.on('timeout_turn', this._finish_selection);
  },
  _messagesReceive(new_msg) {
    var {msgs} = this.state;
    msgs.push(new_msg);
    if (msgs.length > 3) {
      msgs.shift()
    }
    this.setState({msgs});
    console.log('Updated msgs:', msgs, 'after new_msg added', new_msg);
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
      // New turn marked by receiving new actions to choose from
      var active = true;
      this.setState({active});

      var {actions} = this.state;
      actions = proposed_actions;
      this.setState({actions});
      if (actions.length > 0) {
        console.log('Actions[0]', actions[0]);
      } else {
        console.log('No actions were received!', actions);
      }
  },
  _actionsSelected(text) {
      var msg = {role: this.props.role, text: text};
      console.log('Action selected: ', msg);
      socket.emit('action_selected', msg)
  },
  _userSuggestedAction(action_text) {
      console.log('User suggested new action ', action_text);
      // TODO disable choosing other action then suggested?
      socket.emit('new_action', {text: action_text, role: this.props.role, author: this.props.nick})
  },
  _additional_actionReceive(new_action) {
      console.log('Additional action recieved', new_action);
      var {actions} = this.state;
      actions.push(new_action);
      this.setState({actions});
  },
  _finish_selection(msgs) {
      console.log('Finish selection', msgs);
      var active = false;
      var msg = {'style': 'info', 'id': 'local_messages',
          'text': 'Turn finished. Wait for new system response and new actions to choose from!'};
      this._messagesReceive(msg);
      this.state.setState(active);
  },
  _reasons_update(history_dict) {
      var turn_reasons_from_history = [];
      for (var key in history_dict) {
          if (history_dict.hasOwnProperty(key) && (history_dict[key])) {
            turn_reasons_from_history.push(key)
          }
      }
      this.setState(turn_reasons_from_history)
  },
  render() {
      // FIXME grid so it has chance to have enough space
    return (
      <div>
        <div>
          <MsgAnnouncer msgs={this.state.msgs} stats={this.state.stats} />
        </div>
        <Grid>
          <Row className="show-grid">
            <Col xs={4} md={4}>
              <HistoryView active={this.state.active} msgs={this.state.history} onReasonsChanged={this._reasons_update} role={this.props.role} />
            </Col>
            <Col xs={4} md={4}>
              <ActionSelectView active={this.state.active} actions={this.state.actions} new_actions={this.state.new_actions} onSelectedAction={this._actionsSelected} onNewAction={this._userSuggestedAction} notifyUser={this._messagesReceive} />
            </Col>
            <Col xs={4} md={4}>
              <DbView active={this.state.active} />
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
