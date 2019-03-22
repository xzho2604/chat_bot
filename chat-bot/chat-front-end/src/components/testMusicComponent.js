import React from 'react';

const videoItem = () => {
    const url = 'https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3';
    return (
        <div>
            <iframe
                src={url}
                width="300"
                height="380"
                frameBorder="0"
                allowtransparency="true"
                allow="encrypted-media"
                title="test"/>
        </div>
    )
};

export default videoItem;