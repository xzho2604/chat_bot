import React from 'react';

const musicItem = (item) => {
    // If item type is album, return a music list
    if (item.type === 'track') {
        // else return a single song track
        console.log(item);
        return (
            <div>
                <iframe
                    src={item.contents.url}
                    frameBorder="0"
                    width="290"
                    height="80"
                    allowtransparency="true"
                    allow="encrypted-media"
                    title={item.contents.title}/>
            </div>
        )
    } else {
        console.log(item);
        return (
            <div>
                <iframe
                    src={item.contents.url}
                    width="290"
                    height="380"
                    frameBorder="0"
                    allowtransparency="true"
                    allow="encrypted-media"
                    title={item.contents.title}
                />
            </div>
        )
    }
};

export default musicItem;