import React from "react";
import ReactDOM from "react-dom";
import styles from "./ItemCard.module.css";
import Button from "@mui/material/Button";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { getDatabase, ref, set, get, child } from "firebase/database";
import { paperClasses } from "@mui/material";
import GraphPage from "./GraphPage";

class ItemCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datafunc: this.props.databasefunction,
      app: this.props.databaseapp,
    };
  }


  render() {
    return (
      <div className={styles.ItemCard}>
        <div className={styles.ItemCardInfo}>
          <div className={styles.ItemCardTitle}>{this.props.title}</div>
          <div className={styles.ItemCardPrice}>
            {this.props.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") +
              " coins per minute (avg)"}
          </div>
        </div>
      </div>
    );
  }
}


export default ItemCard;
