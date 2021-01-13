// import * as d3 from 'https://d3js.org/d3.v6.min.js';

// d3.select("body").append()
let xmlns = "http://www.w3.org/2000/svg"
let xlink = "http://www.w3.org/1999/xlink"

function createGraph(data, element){
    let svgContainer = document.getElementById(element)
    for (const [key, size] of Object.entries(data)) {
        let i = 1
        let k = key.toString() + "." + i.toString()
        let g = generateSVG("300", "circle", "#003469", "400", key)
        // g.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href")

        let startAngle = 0
        for (const [k, v] of Object.entries(data[key])) {

            //add strokes or something based on lo's within competency
            let loCount = Object.keys(data[key]).length
            let dashArray = (360 / loCount);
            // console.log(dashArray)
            // let rot = (360/ [v].findIndex()).toString()
            // console.log([v])
            let outerCircle = g.getElementById("1."+key.toString())
            let innerCircle = g.getElementById("2."+key.toString());
            let radius = outerCircle.getAttribute("r").toString()
            let strokeColor = ""
            let v2 = [v][0][1]

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
            arc.id = "arc" + key.toString() + i.toString()
            let labelLocationX = (x1 + x2)/2
            let labelLocationY = (y1 + y2)/2
            let label = document.createElementNS(xmlns, "text")
            //label.setAttributeNS(null, "x", labelLocationX.toString())
            //label.setAttributeNS(null, "y", labelLocationY.toString())
            label.setAttributeNS(null, "font-family", "Oswald")
            label.setAttributeNS(null, "fill", "black")
            label.setAttributeNS(null, "font-size", "12pt")
            label.setAttributeNS(null, "font-weight", "500")

            let textNode = document.createTextNode(v[0])

            let labelPath = document.createElementNS(xmlns, "textPath")
            labelPath.setAttributeNS(null, "href", "#" + arc.id)
            labelPath.setAttributeNS(null, "startOffset", "50%")
            labelPath.setAttributeNS(null, "side", "right")
            // labelPath.appendChild(textNode)
            // labelPath.setAttributeNS(xlink, "xlink:href", arc.id)
            labelPath.appendChild(textNode)
            label.appendChild(labelPath)


            ++i;
            // console.log("start angle" + startAngle.toString() + " endAngle: " + endAngle.toString())

            startAngle += dashArray
            // console.log(v2)
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
            g.appendChild(label)
        }
        let svgElem3 = document.createElementNS(xmlns, "circle");
        svgElem3.id = "3." + key;
        svgElem3.setAttributeNS(null, "r", "120")
        svgElem3.setAttributeNS(null, "cx", "150")
        svgElem3.setAttributeNS(null, "cy", "150")
        svgElem3.setAttributeNS(null, "fill", "white")
        svgElem3.setAttributeNS(null, "stroke", "#003469")
        g.appendChild(svgElem3)
        let compWrap = document.createElementNS(xmlns, "foreignObject")
        compWrap.setAttributeNS(null, "width", "150")
        compWrap.setAttributeNS(null, "height", "120")
        compWrap.setAttributeNS(null, "x", "75")
        compWrap.setAttributeNS(null, "y", "75")


        let compLabel = document.createElementNS("http://www.w3.org/1999/xhtml","div")
        let compText = document.createTextNode(key)
        let compLabelPos = "150"
        compLabel.setAttributeNS(null, "class", "compDiv")

        console.log(data[key])
        compLabel.appendChild(compText)
        compWrap.appendChild(compLabel)
        g.appendChild(compWrap)
        // compDiv.appendChild(compLabel)
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
    svgElem.id = "1." + key;
    let sizeControl =  (size / 2.5).toString();
    // if (shape === "circle")
        svgElem.setAttributeNS(null, "r", sizeControl)
        svgElem.setAttributeNS(null, "cx", sizeControl)
        svgElem.setAttributeNS(null, "cy", sizeControl)
        svgElem.setAttributeNS(null, "fill", fill)

    let svgElem2 = document.createElementNS(xmlns, "circle");
    svgElem2.id = "2." + key;
    let sizeControl2 =  (sizeControl / 2).toString();
    svgElem2.setAttributeNS(null, "r", sizeControl2)
    svgElem2.setAttributeNS(null, "cx", sizeControl)
    svgElem2.setAttributeNS(null, "cy", sizeControl)
    svgElem2.setAttributeNS(null, "fill", "none")




    // svgCont.appendChild(svgElem2)
    svgCont.append(svgElem, svgElem2)
    return svgCont
}


function generateCircleChart(data2) {

    //let data = d3.group(data2, d => d.name)
    let data = data2
    //console.log(d3.group(data.Competencies, d => d.name))
    //console.log(d3.group(data, d => d.data.name()))
    let width = 1400
    let height = 1400
    let radius = Math.min(width, height) / 2
    let color = d3.scaleOrdinal(d3.schemeBlues[4])
    let c = d3.scaleThreshold()
        .domain([0.2, 1.1, 3.1])
        .range(["#7f8b85", "#81ce81", "#FF7BAC"])
    let g = d3.select('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')')

    let partition = d3.partition()
        .size([2 * Math.PI, radius ])

    let root = d3.hierarchy(data)
        .sum(function (d) {
            return d.size
        })

    partition(root)



    //let arc = d3.arc()
    //    .startAngle(function(d) { return d.x0 })
    //.endAngle(function(d) { return d.x1 })
    //.innerRadius(function(d) { return d.y0 })
    //.outerRadius(function(d) { return d.y1 })
let x = d3.scaleLinear()
    .domain([0, 1])
    .range([0, 2 * Math.PI])
    let y = d3.scaleLinear()
    .domain([0, 1])
    .range([0, 2 * Math.PI])

let arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .padAngle(d => Math.min((d.x1 - d.x0) / 12, 0.005))
    .padRadius(radius * .4)
    .innerRadius(d => d.y0 )
    .outerRadius(d => d.y1 * .98)
    //.startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
    //.endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
    //.innerRadius(function(d) { return Math.max(0, y(d.y)); })
    //.outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });
    let keyC = [0, 1, 2]


    g.selectAll('path')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr("class", "pathG")
        .append('path')
        .attr("display", function (d) {
            return d.depth ? null : "none"
        })
        .attr("d", arc)
        .style('stroke', 'white')
        .style('fill', function (d) {
            if (d.data.completionLevel) {
                return c(d.data.completionLevel)
            }
            else {
                return "#003469"
            }

        })

    g.selectAll('g.pathG')
        .append("text")
        .text(function (d){return d.data.name})
        .attr("class", "compLabel")
        .attr("y", "1")
        .attr("dy", "0")
        .attr("transform", function(d) {
                        return "translate(" + arc.centroid(d) + ")rotate(" + computeTextRotation(d) + ")";
                })

    g.selectAll('text.compLabel')
        //.call(wrap, 60)
    let svg = d3.select("svg")
}


function computeTextRotation(d) {
        let angle = (d.x0 + d.x1) / Math.PI * 90;

        // Avoid upside-down labels
        //return (angle < 120 || angle > 270) ? angle : angle + 180  // labels as rims
        return (angle < 180) ? angle - 90 : angle + 90  // labels as spokes
}

function wrap(text, width) {
  text.each(function() {
    let text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}