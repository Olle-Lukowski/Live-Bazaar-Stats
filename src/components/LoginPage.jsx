import KeyInput from "./KeyInput";
import Button from "@mui/material/Button";
import React from "react";
import styles from "./LoginPage.module.css";

class LoginPage extends React.Component {

  render() {
    return (
      <div className={styles.LoginPage}>
        <p className={styles.KeyPrompt}>Please enter your API Key.</p>
        <KeyInput />
        <Button variant="contained" onClick={this.props.handleSubmitClick}>Submit</Button>
        <p className="error_message">{this.props.errorMessage}</p>
      </div>
    );
  }
}

export default LoginPage;
