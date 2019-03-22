import React from 'react';

const videoItem = (item) => {
    return (
        <div>
            <iframe
                src={item.url}
                title="TEST"
                allowFullScreen="allowFullScreen"
            />
        </div>
    )
};

export default videoItem;