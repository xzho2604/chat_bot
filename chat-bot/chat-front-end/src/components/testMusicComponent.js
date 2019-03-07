import React from 'react';

const videoItem = () => {
    const url = 'https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3';
    return (
        <div>
            <iframe
                src={url}
                title="TEST"
                frameborder="0"
                allowtransparency="true"
                allow="encrypted-media"
            />
        </div>
    )
};

export default videoItem;