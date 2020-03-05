import React from 'react';
import 'firebase/firestore';

const App = ({ firebase }) => {
    const db = firebase.firestore();
    const messages = db.collection("inbound");
    const test = () => {
        const newMessages = messages.orderBy('timestamp').limit(10);
    };

    return (
        <div className="App">
            <p>Test</p>
            <button onClick={test}>Test</button>
        </div>
    );
};

export default App;
