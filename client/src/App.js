import React from 'react';
import 'firebase/firestore';

const App = ({ firebase }) => {
    const db = firebase.firestore();
    const inbound = db.collection("inbound");
    const test = () => {
        const recentInbound = inbound.orderBy('timestamp').limit(10)
            .get()
            .then(query => {
                query.forEach(doc =>
                    console.log(doc.data())
                )
            })
    };

    return (
        <div className="App">
            <p>Test</p>
            <button onClick={test}>Test</button>
        </div>
    );
};

export default App;
