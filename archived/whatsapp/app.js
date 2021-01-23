var x = d3.csv("./data/whatsAppData.csv", function(err,data){
    if(err) throw err;
    var members=[]

    data.forEach(function(d){
        if(members.indexOf(d.name)==-1){
            members.push(d.name)
        }
    })
    var maxDays = Math.max(...data.map(d => d.day))
    var minDays = Math.min(...data.map(d => d.day))

    var height = 600;
    var width = 1000;
    var paddingx = 130;
    var paddingy = 30;

    yrange=[]
    for(var i=0; i<members.length;i++){

        yrange.push((height-paddingy) - Math.round((height-paddingy)/members.length)*i)
    }

    var yScale = d3.scaleOrdinal()
                    .domain(members)
                    .range(yrange);

    var xScale = d3.scaleLinear()
                    .domain([0,1440])
                    .range([paddingx, width-paddingx]);

    var colorScale = d3.scaleOrdinal()
                        .domain(members)
                        .range(['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
          '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
          '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
          '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
          '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
          '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
          '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
          '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
          '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
          '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'])

    var xAxis = d3.axisBottom(xScale)
                    .tickSize(-height + 2*paddingy)
    var yAxis = d3.axisLeft(yScale)
                    .tickSize(-width + 2*paddingx)
    d3.select("svg")
        .attr("width",width)
        .attr("height",height)

    d3.select("svg")
        .append("g")
        .attr("transform","translate(0,"+(height-paddingy)+")")
        .call(xAxis)

    d3.select("svg")
        .append("g")
        .attr("transform","translate("+(paddingx)+",0)")
        .call(yAxis)

    d3.select("svg")
        .append("text")
        .text("Minute")
            .attr("y",height-paddingy+(paddingy))
            .attr("x",(width-paddingx)/2)

    var tooltip = d3.select("body")
                    .append("div")
                    .classed("tooltip",true)

    function update(day){
        var temp = data.filter(d => d.day==day)
        var rScale = d3.scaleLinear()
                        .domain(d3.extent(temp, d => d.message.length))
                        .range([2.5,50])

        var circles = d3.select("svg")
                        .selectAll("circle")
                        .data(temp,d => d.day)

        circles
            .exit()
            .remove()

        circles
            .enter()
            .append("circle")
            .on("mouseover",function(d){
                tooltip
                    .style("opacity",1)
                    .style("left",d3.event.x+"px")
                    .style("top",d3.event.y+"px")
                    .html("<p>"+"<strong>"+d.name+":"+"</strong>"+"<br>"+d.message+"<br>"+"<strong>"+"Time:"+"</strong>"+"<br>"+Math.round(d.time/60)+":"+d.time%60+"</p>");
            })
            .on("mouseout", function(){
                tooltip
                    .style("opacity",0)
            })
                .attr("stroke","#fff")
                // .attr("fill",d => colorScale(d.name))
                .attr("cy",d => yScale(d.name))
                .attr("r", 7.5 )
                .transition()
                    .duration(500)
                    .delay((d, i) => i * 5)
                    .attr("cx",d => xScale(d.time))
        var date = temp[0]["date"]
        d3.select(".date")
            .text(date)
    }

    update(13)

    d3.select("input")
        .property("max",maxDays)
        .property("min",minDays)
        .property("value",13)
        .on("input", function(){
            console.log(+d3.event.target.value)
            update(+d3.event.target.value)
        })
})


