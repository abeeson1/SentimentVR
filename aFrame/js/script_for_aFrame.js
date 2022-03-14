//get the whole a-scene
    const aScene = document.querySelector('a-scene');



//Create the seven layers: 64, 32, 16, 8, 4, 2, 1
    const yInterval_initial = -10,
          yInterval = 5,
          numbersOfTemas = [64, 32, 16, 8, 4, 2, 1],
          rotationAngleFactor = Math.PI / (numbersOfTemas[0] / 2),
          maxR = 10;

    //create each round
        for(let i = 0; i < 7; i ++){
            let numberOfTeams = numbersOfTemas[i],
                thisRound = document.createElement('a-entity');
            thisRound.setAttribute('id', `round_${numberOfTeams}`);
            thisRound.setAttribute('position', `0 ${yInterval_initial + i * yInterval} -15`);
            aScene.appendChild(thisRound);

            // create the detail in each round
                for(let j = 0; j < numberOfTeams; j ++){
                    //create the sphere
                        // create a sphere representing one team
                            let aSphere = document.createElement('a-sphere');
                            aSphere.setAttribute('color','blue');
                            aSphere.setAttribute('scale','0.1 0.1 0.1');
                        // generate the parameters for the entity
                            let thisR = Math.random() * maxR;     // returns a random number from 0 to maxR
                            let xPosition = Math.cos(rotationAngleFactor * j) * thisR;
                            let zPosition = Math.sin(rotationAngleFactor * j) * thisR;
                        // set the parameter to the entity to adjust its position
                            aSphere.setAttribute('position', `${xPosition} 0 ${zPosition}`);

                    //create the circle
                        // create a circle to identify its R
                            let aCircle = document.createElement('a-circle');
                        // set basic parameters
                            aCircle.setAttribute('wireframe', 'true');
                            aCircle.setAttribute('color', 'yellow');
                            aCircle.setAttribute('opacity', 0.1);
                            aCircle.setAttribute('rotation', '90 0 0');

                        // set customized parameters
                            aCircle.setAttribute('radius', thisR);

                    // add the rGuideCircle and the entity into the layer it belongs to
                        thisRound.appendChild(aCircle)
                        thisRound.appendChild(aSphere);
                }
            }



// interaction
    const spheres = document.querySelectorAll('a-sphere');
    spheres.forEach((s) => {
        s.addEventListener('mouseenter', function(){
            this.setAttribute('opacity', 0.5);
        })
        s.addEventListener('mouseleave', function(){
            this.setAttribute('opacity', 1);
        })
    })
