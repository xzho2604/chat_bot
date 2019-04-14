import React from 'react';

const musicItem = (item) => {
    // If item type is album, return a music list
    if (item.type === 'track') {
        // else return a single song track
        return (
            <div>
                <iframe
                    src={item.url}
                    frameBorder="0"
                    width="290"
                    height="80"
                    allowtransparency="true"
                    allow="encrypted-media"
                    title={item.title}/>
            </div>
        )
    } else {
        return (
            <div>
                <iframe
                    src={item.url}
                    width="290"
                    height="380"
                    frameBorder="0"
                    allowtransparency="true"
                    allow="encrypted-media"
                    title={item.title}
                />
            </div>
        )
    }
};

export default musicItem;