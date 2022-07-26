import React from "react";
import styles from './KeyInput.module.css';

function KeyInput(){
    return (
        <div>
            <input type="text" className={styles.KeyInput}/>
        </div>
    );
}

export default KeyInput;