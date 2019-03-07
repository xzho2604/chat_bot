import React from 'react';

const videoItem = () => {
    const url = 'https://www.youtube.com/embed/0LHxvxdRnYc';
    return (
        <div>
            <iframe
                src={url}
                title="TEST"
                allowFullScreen="allowFullScreen"
            />
        </div>
    )
};

export default videoItem;