import React from 'react';
import './TestLoading.css';
import { Spin, Icon } from 'antd';
class TestLoading extends React.Component {
    state = {
        loading: true
    };
    render() {
        const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin />;

        return (
            <div className="container">
                <Spin indicator={antIcon} />
            </div>
        )
    }
}

export default TestLoading;