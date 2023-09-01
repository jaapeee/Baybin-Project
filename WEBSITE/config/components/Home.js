import React, { useState, useEffect}from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import figure1 from '../Images/figure1.jpg'
import figure2 from '../Images/figure2.png'
import anemone from '../Gifs/anemone.gif'
import './Home.css'
import { database  } from '../config/firebase'
import { onValue, ref,  } from 'firebase/database'


function Home() {

    const [cycle, setCycle] = useState([]);
    const [baybin, setBaybin] = useState([]);
    const [water, setWater] = useState([]);
    const [oil, setOil] = useState([]);
    const [oxide, setOxide] = useState([]);
    const [hourly, setHourly] = useState([]);
    const [daily, setDaily] = useState([]);

    useEffect(() => {
      const cycleRef= ref(database, 'no_of_cycles/');
      const baybinRef = ref(database, 'seabin_content/');
      const waterRef = ref(database, 'water_level/');
      const oilRef = ref(database, 'oil_level/');
      const oxideRef = ref(database, 'oxide_level/');
      const hourlyRef= ref(database, 'waste_collected_per_hour/');
      const dailyRef= ref(database, 'daily_waste_collected/');

      const cycleListener = onValue(cycleRef, (snapshot) => {
        setCycle(snapshot.val());
      });
      const baybinListener = onValue(baybinRef, (snapshot) => {
        setBaybin(snapshot.val());
      });
      const waterListener = onValue(waterRef, (snapshot) => {
        setWater(snapshot.val());
      });
      const oilListener = onValue(oilRef, (snapshot) => {
        setOil(snapshot.val());
      });
      const oxideListener = onValue(oxideRef, (snapshot) => {
        setOxide(snapshot.val());
      });
      const hourlyListener = onValue(hourlyRef, (snapshot) => {
        setHourly(snapshot.val());
      });
      const dailyListener = onValue(dailyRef, (snapshot) => {
        setDaily(snapshot.val());
      });


      return () => {
        cycleListener();
        baybinListener();
        waterListener();
        oilListener();
        oxideListener();
        hourlyListener();
        dailyListener();
      };
    }, []);
  return (
    <>
    <div class="title_page row">
            <div class="title_text col text-center my-auto">
                <h1 class="">Baybin</h1>
                <h2 class="">Real-time Seabin Monitoring System</h2>
            </div>
        </div>
        
        <div class="page_break_1 row"></div>
        <div class="stmt_page row text-centers justify-content-evenly">
            <div class="figure1_container col-md-5 my-auto text-center">
                <div class="figure1 col">
                    <img src={figure1} alt='figure1' class="background my-auto img-fluid"/>
                    <img src={anemone} class="foreground img-fluid"/>
                </div>  
            </div>

            <div class="col-md-5 my-auto">
                <div class="stmt_text row text-center mx-3">
                    <h3>Committed to cleaning up coastlines and more.</h3> 
                    <p>Seabin is a floating garage bin that collects and skims litter from the water by using a filter mechanism, powered by a waterpump. The Seabin are more commonly situated to water systems that are located adjacent to highly – polulated zones such as ports and marinas.</p>
                </div>
            </div>
        </div>
        <div class="page_break_4 row">
        </div>

        <div class="dashboard_page_1 row d-flex flex-column">
            <div class="dash_container row my-auto d-flex justify-content-center">
                
                <div class="dash_container_panel1 col-xl-4 d-flex flex-column">
                    <div class="row flex-fill mb-4">
                        <div class="col dash_data dash_data_left d-flex align-items-center text-center">
                            <div class="row mx-auto">
                                <h2>Total Number of Cycles</h2>
                                <h1 class="my-2"> {cycle} </h1>
                                <h5>Cycle/s</h5>
                            </div>
                        </div>
                    </div>
                    <div class="row flex-fill mb-4">


                        <div class="col dash_data dash_data_left d-flex me-4">
                            <div class="row mx-auto">
                                <div class="row align-items-center text-center">

                                    <div class="col">
                                        <div class="sbin-cont col-12"> 
                                            {water} 
                                        </div>
                                        <h3 class="col-12"> Water Level</h3>
                                    </div>

                                </div>
                            </div> 
                        </div>


                        <div class="col dash_data dash_data_left d-flex">
                            <div class="row mx-auto">
                                <div class="row align-items-center text-center">
                                    <div class="col">
                                        <div class="sbin-cont col-12"> 
                                            {baybin} 
                                        </div>
                                        <h3 class="col-12">Bin Level</h3>
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                    <div class="row flex-fill">
                        <div class="col dash_data dash_data_left d-flex me-4">
                            <div class="row mx-auto">
                                <div class="row align-items-center text-center">
                                    <div class="col">
                                        <div class="sbin-cont col-12"> 
                                            {oil} 
                                         </div>
                                        <h3 class="col-12">Iron Oxide Level</h3>
                                    </div>
                                 
                                </div>
                                
                            </div>
                        </div>
                        <div class="col dash_data dash_data_left d-flex ">
                            <div class="row mx-auto">
                                <div class="row align-items-center text-center">
                                    <div class="col">
                                        <div class="sbin-cont col-12"> 
                                            {oxide} 
                                        </div>
                                        <h3 class="col-12">Oil Level</h3>
                                    </div>

                                </div>
                            
                            </div>
                       
                        </div>
                    </div>
                </div>
    
                <div class="dash_container_panel2 col-xl-7 d-flex flex-column">
                    <div class="row flex-fill ms-5 mb-4">
                        <div class="col dash_data dash_data_right d-flex align-items-center text-center">
                            <div class="row mx-auto">
                                <h2><b>Waste collected per hour</b></h2>
                                <h1 class="my-3">{hourly}</h1>
                                <h5> Kilogram/s</h5>
                            </div>
                        </div>
                    </div>
                    <div class="row flex-fill ms-5">
                    <div class="col dash_data dash_data_right d-flex align-items-center text-center">
                            <div class="row mx-auto">
                                <h2><b>Daily waste collected</b></h2>
                                <h1 class="my-3">{daily}</h1>
                                <h5> Kilogram/s</h5>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="page_break_3 row">
        </div>

        <div class="quote_page row">
            <div class="quote_container row my-auto justify-content-center d-flex flex-row-reverse">
                <div class="col-md-5 text-center">
                    <div class="figure2">
                        <img src={figure2} alt='figure2' unselectable="true" srcset=""/>
                    </div>
                </div>

                <div class="quote_text col-md-5 text-center my-auto">
                    <figure class="mb-5">
                        <blockquote class="blockquote">
                            <p>"No water, no <b>life</b>.<br/> No <b>blue</b>, no green."</p>
                        </blockquote>
                        <figcaption class="blockquote-footer">
                            Sylvia Earle
                        </figcaption>
                    </figure>

                    <h5> Help us make a difference.</h5>
                </div>
                
            </div>

        </div>
        
        </>  
  )
}

export default Home
