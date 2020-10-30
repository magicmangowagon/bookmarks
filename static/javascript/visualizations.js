// import * as d3 from 'https://d3js.org/d3.v6.min.js';

// d3.select("body").append()
let xmlns = "http://www.w3.org/2000/svg"

function createGraph(data, element){
    let svgContainer = document.getElementById(element)
    for (const [key, value] of Object.entries(data)) {
        let g = generateSVG("300", "circle", "#003469", "400", key)
        let i = 1
        let startAngle = 0
        for (const [k, v] of Object.entries(data[key])) {

            //add strokes or something based on lo's within competency
            let loCount = Object.keys(data[key]).length
            let dashArray = (360 / loCount);
            console.log(dashArray)
            // let rot = (360/ [v].findIndex()).toString()
            console.log([v])
            let outerCircle = g.getElementById("1."+key.toString())
            let innerCircle = g.getElementById("2."+key.toString());
            let radius = outerCircle.getAttribute("r").toString()
            let strokeColor = ""
            let v2 = [v][0]

            let testNo = 150
            let endAngle = startAngle + dashArray
            let y1 = parseInt(testNo + 180*Math.sin(Math.PI*startAngle/180));
            let y2 = parseInt(testNo + 180*Math.sin(Math.PI*endAngle/180));
            let x1 = parseInt(testNo + 180*Math.cos(Math.PI*startAngle/180));
            let x2 = parseInt(testNo + 180*Math.cos(Math.PI*endAngle/180));
            let arc = document.createElementNS(xmlns, "path")
            arc.setAttributeNS(null, "d", "M"+ "150" + ","
                + "150" + " L" + x1.toString()+ "," + y1.toString() + " A180,180 "  +  " 0 0,1 " +
                x2.toString()+ "," + y2.toString() + " z")
            ++i;
            console.log("start angle" + startAngle.toString() + " endAngle: " + endAngle.toString())

            startAngle += dashArray
            console.log(v2)
            if (v2 === 2) {
                strokeColor = "#00a497"
            }
            if (v2 === 1) {
                strokeColor = "pink"
            }
            if (v2 === 0) {
                strokeColor = "gray"
            }
            arc.setAttributeNS(null, "fill", strokeColor)
            arc.setAttributeNS(null, "stroke", "#003469")
            g.appendChild(arc)
            innerCircle.setAttributeNS(null, "stroke", strokeColor)
            innerCircle.setAttributeNS(null, "stroke-width", outerCircle.getAttribute("r").toString())
            innerCircle.setAttributeNS(null, "stroke-dasharray", dashArray + " 1")
        }
        let svgElem3 = document.createElementNS(xmlns, "circle");
        svgElem3.id = "3." + key.toString();
        svgElem3.setAttributeNS(null, "r", "75")
        svgElem3.setAttributeNS(null, "cx", "150")
        svgElem3.setAttributeNS(null, "cy", "150")
        svgElem3.setAttributeNS(null, "fill", "white")
        svgElem3.setAttributeNS(null, "stroke", "#003469")
        g.appendChild(svgElem3)
        svgContainer.appendChild(g)
    }
}

//handy dandy function for creating basic shapes
function generateSVG(size, shape, fill, viewport, key) {

    // create svg viewBox for each competency
    let svgCont = document.createElementNS(xmlns, "svg")
    svgCont.setAttributeNS(null, "width", size)
    svgCont.setAttributeNS(null, "height", size)
    svgCont.setAttributeNS(null, "viewBox", "-40 -40 " + viewport + " " + viewport)

    // add shape to each viewBox, turn this into a switch statement/dict or something
    // basically writing my own viz library at this point...
    let svgElem = document.createElementNS(xmlns, shape);
    svgElem.id = "1." + key.toString();
    let sizeControl =  (size / 2.5).toString();
    // if (shape === "circle")
        svgElem.setAttributeNS(null, "r", sizeControl)
        svgElem.setAttributeNS(null, "cx", sizeControl)
        svgElem.setAttributeNS(null, "cy", sizeControl)
        svgElem.setAttributeNS(null, "fill", fill)

    let svgElem2 = document.createElementNS(xmlns, "circle");
    svgElem2.id = "2." + key.toString();
    let sizeControl2 =  (sizeControl / 2).toString();
    svgElem2.setAttributeNS(null, "r", sizeControl2)
    svgElem2.setAttributeNS(null, "cx", sizeControl)
    svgElem2.setAttributeNS(null, "cy", sizeControl)
    svgElem2.setAttributeNS(null, "fill", "none")




    // svgCont.appendChild(svgElem2)
    svgCont.append(svgElem, svgElem2)
    return svgCont
}

