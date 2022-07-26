import LoginPage from "./components/LoginPage";
import React from "react";
import MainPage from "./components/MainPage";


class App extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    return (
      <div className="App">
        <MainPage />
      </div>
    );
  }
}

export default App;
