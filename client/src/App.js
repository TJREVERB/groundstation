import React from 'react';
import 'firebase/firestore';

const App = ({ firebase }) => {
    const db = firebase.firestore();
    const test = () => {
        db.collection('inbound')
            .get()
            .then(querySnapshot => {
                querySnapshot.forEach(doc => {
                    console.log(`${doc.id} => ${JSON.stringify(doc.data())}`);
                });
            });
    };

    return (
        <div className="App">
            <p>Test</p>
            <button onClick={test}>Test</button>
        </div>
    );
};

export default App;
