import React from 'react';

const videoItem = (item) => {
    return (
        <div>
            <iframe
                src={item.url}
                title="TEST"
                width="290"
                height="300"
                allowFullScreen="allowFullScreen"
            />
        </div>
    )
};

export default videoItem;