From Human-Human to Human-System Dialogue.
==========================================

A proof of concept for bootstrapping an end-to-end system with with annotated data throughout a pipeline of the system.
Annotated are collected using crowdsourcing.

Todos & remarks
----------------

- UI design
    - Combine react and bootstrap http://react-bootstrap.github.io/components.html
    - React official doc is enough: http://facebook.github.io/react/docs/thinking-in-react.html
    - TODO load data from flask via websockets
    - TODO login and integration with crowdflower
    - how to get immediate feedback
    - Select one from list http://stackoverflow.com/questions/27512180/reactjs-onclick-event-how-to-select-a-specific-button-from-a-list
- Model - DB columns, different attention - I need to use columns
    - negative examples - distribute to (no one selected actions - 0 probability, selected action receives probability of changing the "future" - computed after dialog using another & reversed RNN choosing only from the selected actions
- if support for proper authentication wanted look at fbone or at https://github.com/gae-init/gae-init/blob/master/main/auth/auth.py
- mail smtp error handler. setup email bootai-admin@gmail.com and use this tutorial http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
- TODO manage session via decorators and invalidate sessions if role and dialogue is not valid anymore and make it expire quite soon e.g. after few hours http://stackoverflow.com/questions/11783025/is-there-an-easy-way-to-make-sessions-timeout-in-flask
- implement CountDown and TIMEOUTS for waiting on other side action-selection using https://github.com/shanealynn/async_flask/blob/master/application.py
- Example app with eventlet side pushing of notification https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py

- TODO TESTS
    - 1. login 2. assign new dialog 3. check that 
        - dialog_id and role is assign
        - socketio connection is loaded and receiving messages both ways
    - artificially setup user session and check login of socketio communication
    - artificially setup two sessions and check that users and assistant member can communicate
    - artificially setup three sessions (2 assistants and one user) and check that user and assistants member can communicate
    - previous example vice versa 1 assistant and 2 users
