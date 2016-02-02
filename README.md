Journey from Human to Human to Human to System Dialogue - There and Back Again
==============================================================================

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
    - negative examples - distribute to (no one selected actions - 0 probability, selected action receives probability of changing the "future" - computed after dialogue using another & reversed RNN choosing only from the selected actions
