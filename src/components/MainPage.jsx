import React from "react";
import styles from "./MainPage.module.css";
import LoginPage from "./LoginPage";
import ItemCard from "./ItemCard";
import ItemCardGraphs from "./ItemCardGraphs";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, set, get, child} from "firebase/database";
import GraphPage from "./GraphPage";
import { Button } from "@mui/material";
class MainPage extends React.Component {
  constructor(props) {
    super(props);
    const firebaseConfig = {

        apiKey: "AIzaSyCYmm2l56LkPhB2o6FmakhioBnfHslkq7U",
      
        authDomain: "live-bazaar-stats.firebaseapp.com",
      
        projectId: "live-bazaar-stats",
      
        storageBucket: "live-bazaar-stats.appspot.com",
      
        messagingSenderId: "38601534331",
      
        appId: "1:38601534331:web:f37873a4cf1d4b65a2abde",
        dataBaseURL: "https://live-bazaar-stats-default-rtdb.firebaseio.com/",
      };      
    this.state = {
      graphPage: [],
      graphsShown: false,
      ApiKey: "",
      ErrorMessage: "",
      productCards: [],
      app : initializeApp(firebaseConfig),
      data : [],
    };
  }

  handleSubmitClick = () => {
    this.setState({
      ApiKey: document.getElementsByClassName("KeyInput").value,
    });
    fetch(
      "https://api.hypixel.net/skyblock/bazaar?Api-Key=" + this.state.ApiKey
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.setState({
            ErrorMessage: "",
          });
        } else {
          this.setState({
            ErrorMessage: "Invalid API Key, too many requests or API is down.",
          });
        }
      });
    document.getElementsByClassName("LoginPage")[0].style.display = "none";
    this.updateDatabase();
    this.displayProducts();
    setTimeout(() => {
      this.setCardDataBase();
    }
    , 1000);
    setInterval(() => {
        this.updateDatabase();
    }, 300000);
    setTimeout(() => {
    setInterval(() => {
        this.displayProducts();
    }, 30000);
    }
    , 2000);
    setTimeout(() => {
      setInterval(() => {
      this.setCardDataBase();
      }
      , 30000);
    }
    , 3000);
  };

  callFuncs = () => {
    this.displayProducts();
    this.setCardDataBase();
  }


  displayProducts = () => {
    let self = this;
        let newProductCards = [];
    fetch(
      "https://api.hypixel.net/skyblock/bazaar?Api-Key=" + this.state.ApiKey
    )
      .then((response) => response.json())
      .then((data) => {
        if (data["success"]) {
          let products = data["products"];
          Object.keys(products).forEach(function (i) {
            if (
              products[i]["buy_summary"][0] != undefined &&
              products[i]["sell_summary"][0] != undefined
            ) {
              let buyPrice = JSON.parse(
                JSON.stringify(products[i]["buy_summary"][0]["pricePerUnit"])
              );
              let sellPrice = JSON.parse(
                JSON.stringify(products[i]["sell_summary"][0]["pricePerUnit"])
              );
              let buyMovingWeek = products[i]["quick_status"]["buyMovingWeek"];
              buyMovingWeek = buyMovingWeek / 7 / 24 / 60;
              let sellMovingWeek =
                products[i]["quick_status"]["sellMovingWeek"];
              sellMovingWeek = sellMovingWeek / 7 / 24 / 60;

              let profitPerMinute =
                buyPrice * 0.9875 * Math.min(sellMovingWeek, buyMovingWeek) -
                sellPrice * Math.min(sellMovingWeek, buyMovingWeek);
              profitPerMinute = Math.round(profitPerMinute * 10) / 10;
              newProductCards.push(
                <ItemCardGraphs
                  key={i}
                  title={i}
                  price={profitPerMinute}
                />
              );
            }
          });
          newProductCards.sort(function (a, b) {
            return parseFloat(b.props.price) - parseFloat(a.props.price);
          });
          return newProductCards;
        } else {
          return <p>{this.state.ErrorMessage}</p>;
        }
      })
      .then((data) => {
        this.setState({
          productCards: data,
        });
      });
  };

    setCardDataBase = () => {
        let cards = [];
      for (let i = 0; i < this.state.productCards.length; i++) {

        let card = this.state.productCards[i];
        let title = card.props.title;
        let price = card.props.price;
        let databaseapp = this.state.app;
        cards.push(<ItemCardGraphs key={title} title={title} price={price} databaseapp={databaseapp}/>);
        }
        this.setState({
            productCards: cards,
        });
    }


  updateDatabase = () => {
    let database = getDatabase(this.state.app);
    let currentTime = new Date();
    let currentTimeString =
        currentTime.getUTCFullYear() +
        "-" +
        (currentTime.getUTCMonth() + 1) +
        "-" +
        currentTime.getUTCDate() +
        " " +
        currentTime.getUTCHours() +
        ":" +
        currentTime.getUTCMinutes();
    fetch(
      "https://api.hypixel.net/skyblock/bazaar?Api-Key=" + this.state.ApiKey
    )
      .then((response) => response.json())
      .then((data) => {
        if (data["success"]) {
          let products = data["products"];
          return products;
        } else {
          console.log("Error");
        }
      }
      ).then((products) => {
        for (let product in products) {
          if (products[product]["buy_summary"][0] != undefined && products[product]["sell_summary"][0] != undefined) {
            set(ref(database, "data/" + product + "/buyPricePerUnit/" + currentTimeString), JSON.parse(JSON.stringify(products[product]["buy_summary"][0]["pricePerUnit"])));
            set(ref(database, "data/" + product + "/sellPricePerUnit/" + currentTimeString), JSON.parse(JSON.stringify(products[product]["sell_summary"][0]["pricePerUnit"])));
            set(ref(database, "data/" + product + "/buyMovingWeek/" + currentTimeString), JSON.parse(JSON.stringify(products[product]["quick_status"]["buyMovingWeek"])));
            set(ref(database, "data/" + product + "/sellMovingWeek/" + currentTimeString), JSON.parse(JSON.stringify(products[product]["quick_status"]["sellMovingWeek"])));
        }
      }
      }
      );
  }
        

  
  render() {
    return (
      <div className={styles.TitleHeader}>
        <h1>Live Bazaar Stats</h1>
        {this.state.graphPage}
        <LoginPage
          handleSubmitClick={this.handleSubmitClick}
          errorMessage={this.state.ErrorMessage}
        />
        <div className={styles.ProductDisplay}>{this.state.productCards}</div>
      </div>
    );
  }
}

export default MainPage;
