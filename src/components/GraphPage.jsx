import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { getDatabase, ref, set, get, child } from "firebase/database";
import React from "react";
import { Button } from "@mui/material";
import styles from "./GraphPage.module.css";

class GraphPage extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            app: this.props.databaseapp,
            graphBuyPrice: undefined,
            graphSellPrice: undefined,
            graphBuyMovement: undefined,
            graphSellMovement: undefined,
        }
    }

    async await_response(product, requested_data) {
        let response = await this.getDataForProduct(product, requested_data);
        return response;
      }
    
    
      viewGraphs = () => {
        const DataFormater = (number) => {
            if(number > 1000000000){
              return (number/1000000000).toString() + 'B';
            }else if(number > 1000000){
              return (number/1000000).toString() + 'M';
            }else if(number > 1000){
              return (number/1000).toString() + 'K';
            }else{
              return number.toString();
            }
          }
        let productBuyData = this.await_response(
          this.props.title,
          "buyPricePerUnit"
        );
        let productBuyMovingData = this.await_response(
            this.props.title,
            "buyMovingWeek"
        );
        let productSellData = this.await_response(
            this.props.title,
            "sellPricePerUnit"
        );
        let productSellMovingData = this.await_response(
            this.props.title,
            "sellMovingWeek"
        );
    
        let productBuyDataArray = [];
        let productBuyMovingDataArray = [];
        let productSellDataArray = [];
        let productSellMovingDataArray = [];
        this.fillDataArrayBuyPrice(function (data) {
          Object.keys(data).forEach((key) => {
            productBuyDataArray.push({
              time: key,
              value: data[key],
            });
          }
          );
          if (productBuyDataArray !== undefined) {
            
            return ({
              graphBuyPrice: (
                <div className={styles.miniContainer}>
                <p className={styles.title}>Buy Price</p>
                <LineChart
                  width={500}
                  height={250}
                  className={styles.graph}
                  data={productBuyDataArray}
                  margin={{
                    top: 15,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <YAxis tickFormatter={DataFormater}/>
                  <Tooltip/>
                  <Line type="monotone" dataKey="value" stroke="#8884d8" />
                </LineChart>
                </div>
              ),
            });
          }
          else {
            return ({
              graphBuyPrice: <div>Loading...</div>,
            });
          }
        }, productBuyData);

        this.fillDataArrayBuyMoving(function (data) {
            Object.keys(data).forEach((key) => {
              productBuyMovingDataArray.push({
                time: key,
                value: data[key],
              });
            }
            );
            if (productBuyMovingDataArray !== undefined) {
              
              return ({
                graphBuyMovement: (
                    <div className={styles.miniContainer}>
                <p className={styles.title}>Buy Movement</p>
                  <LineChart
                    width={500}
                    height={250}
                    className={styles.graph}
                    data={productBuyMovingDataArray}
                    margin={{
                      top: 15,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <YAxis tickFormatter={DataFormater}/>
                    <Tooltip/>
                    <Line type="monotone" dataKey="value" stroke="#8884d8" />
                  </LineChart>
                  </div>
                ),
              });
            }
            else {
              return ({
                graphBuyMovement: <div>Loading...</div>,
              });
            }
          }, productBuyMovingData);
        
          this.fillDataArraySellPrice(function (data) {
            Object.keys(data).forEach((key) => {
              productSellDataArray.push({
                time: key,
                value: data[key],
              });
            }
            );
            if (productSellDataArray !== undefined) {
              
              return ({
                graphSellPrice: (
                    <div className={styles.miniContainer}>
                <p className={styles.title}>Sell Price</p>
                  <LineChart
                    width={500}
                    height={250}
                    className={styles.graph}
                    data={productSellDataArray}
                    margin={{
                      top: 15,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <YAxis tickFormatter={DataFormater}/>
                    <Tooltip/>
                    <Line type="monotone" dataKey="value" stroke="#8884d8" />
                  </LineChart>
                    </div>
                ),
              });
            }
            else {
              return ({
                graphSellPrice: <div>Loading...</div>,
              });
            }
          }, productSellData);
          
          this.fillDataArraySellMoving(function (data) {
            Object.keys(data).forEach((key) => {
              productSellMovingDataArray.push({
                time: key,
                value: data[key],
              });
            }
            );
            if (productSellMovingDataArray !== undefined) {
              
              return ({
                graphSellMovement: (
                    <div className={styles.miniContainer}>
                    <p className={styles.title}>Sell Movement</p>
                  <LineChart
                    width={500}
                    height={250}
                    className={styles.graph}
                    data={productSellMovingDataArray}
                    margin={{
                      top: 15,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <YAxis tickFormatter={DataFormater}/>
                    <Tooltip/>
                    <Line type="monotone" dataKey="value" stroke="#8884d8" />
                  </LineChart>
                  </div>
                ),
              });
            }
            else {
              return ({
                graphSellMovement: <div>Loading...</div>,
              });
            }
          }, productSellMovingData);
      };
      
      

      async fillDataArrayBuyPrice(callback, data){
        await data.then((value) => {
          let graphs = callback(value);
          this.setState({
            graphBuyPrice: graphs.graphBuyPrice,
          });
        }
        );
      };
      async fillDataArrayBuyMoving(callback, data){
        await data.then((value) => {
          let graphs = callback(value);
          this.setState({
            graphBuyMovement: graphs.graphBuyMovement,
          });
        }
        );
      };
      async fillDataArraySellPrice(callback, data){
        await data.then((value) => {
          let graphs = callback(value);
          this.setState({
            graphSellPrice: graphs.graphSellPrice,
          });
        }
        );
      };
      async fillDataArraySellMoving(callback, data){
        await data.then((value) => {
          let graphs = callback(value);
          this.setState({
            graphSellMovement: graphs.graphSellMovement,
          });
        }
        );
      };
    
      getDataForProduct = (product, requestedData) => {
        let database = getDatabase(this.state.app);
    
        console.log(database);
        let data = undefined;
        let dbref = ref(database);
        data = get(child(dbref, "data/" + product + "/" + requestedData))
          .then((snapshot) => {
            if (snapshot.exists()) {
              return snapshot.val();
            } else {
              console.log("No data available");
            }
          })
          .catch((error) => {
            console.error(error);
          });
        return data;
      };

    render(){
        return(
            <div>
            <div className={styles.container}>
                    {this.state.graphBuyPrice}
                    {this.state.graphBuyMovement}
                
            </div>
            <div className={styles.container}>
                    {this.state.graphSellPrice}
                    {this.state.graphSellMovement}
                
            </div>
            <Button variant="contained" onClick={this.viewGraphs}>View Graphs</Button>
            </div>
        )
    }
}

export default GraphPage;