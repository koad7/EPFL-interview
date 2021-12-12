var geoCoordMap = {
    "Chi_and_Uang_2002_DC2":[6.633597, 46.519962],
    "Engelhardt_et_al_2000_DBBW":[6.15613, 46.598813],
    "Engelhardt_et_al_2000_DBBWWPZ":[6.15613, 46.698813],
    "Engelhardt_et_al_2000_DBWW":[6.90613, 46.998813],
    "Lee_et_al_2002_CR1":[6.50613, 45.998813],
    "Lee_et_al_2002_CR2":[6.40613, 45.898813],
    "Del_Caprio_et_al_2014_RBS-A":[6.00613, 46.898813],
    "Ciutina_and_Dubina_2008_CP-R-M" :[6.49613, 46.508813],
    "Ciutina_and_Dubina_2008_CP-IIPL-M":[6.45613, 46.528813],
    "Kosarieh_and_Danesh_2016_SN1":[6.10613, 46.198813],
    "Kosarieh_and_Danesh_2016_SN2":[6.10613, 46.128813]
  };
  
  var data = [
    {name: "Chi_and_Uang_2002_DC2" , value:'Exterior_Subassembly'},            
    {name: "Engelhardt_et_al_2000_DBBW" , value:'Interior_Subassembly' },       
    {name: "Engelhardt_et_al_2000_DBBWWPZ", value:'Interior_Subassembly' },    
    {name: "Engelhardt_et_al_2000_DBWW" , value:'Exterior_Subassembly' },      
    {name: "Lee_et_al_2002_CR1" , value:'Exterior_Frame' },               
    {name: "Lee_et_al_2002_CR2" , value:'Exterior_Frame' },               
    {name: "Del_Caprio_et_al_2014_RBS-A", value:'Exterior_Frame' },      
    {name: "Ciutina_and_Dubina_2008_CP-R-M"  , value:'Exterior_Frame' },  
    {name: "Ciutina_and_Dubina_2008_CP-IIPL-M", value:'Exterior_Subassembly' },
    {name: "Kosarieh_and_Danesh_2016_SN1"  , value:'Exterior_Subassembly' },    
    {name: "Kosarieh_and_Danesh_2016_SN2" , value:'Exterior_Subassembly' }
  ];
  
  var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
      var geoCoord = geoCoordMap[data[i].name];
      if (geoCoord) {
        res.push({
          name: data[i].name,
          value: geoCoord.concat(data[i].value)
        });
      }
    }
    return res;
  };
  
  var convertedData = [
    convertData(data),
    convertData(
      data
        .sort(function (a, b) {
          return b.value - a.value;
        })
        .slice(0, 6)
    )
  ];
  console.log(convertedData);
  // based ready dom, initialize echarts instance
  var chart = echarts.init(document.getElementById("main"));
  
  option = {
    backgroundColor: "#404a59",
    animation: false,
    title: [
      {
        text: "Homework EPFL Full Stack",
        subtext: "IT4Research",
        sublink: "Kodjo",
        left: "center",
        textStyle: {
          color: "#fff"
        }
      },
      {
        id: "statistic",
        right: 120,
        top: 40,
        width: 100,
        textStyle: {
          color: "#fff",
          fontSize: 16
        }
      }
    ],
    toolbox: {
      iconStyle: {
        normal: {
          borderColor: "#fff"
        },
        emphasis: {
          borderColor: "#b1e4ff"
        }
      }
    },
    brush: {
      outOfBrush: {
        color: "#abc"
      },
      brushStyle: {
        borderWidth: 2,
        color: "rgba(0,0,0,0.2)",
        borderColor: "rgba(0,0,0,0.5)"
      },
      seriesIndex: [0, 1],
      throttleType: "debounce",
      throttleDelay: 300,
      geoIndex: 0
    },
    geo: {
      map: "world",
      left: "10",
      right: "35%",
      center: [6.633597, 46.519962],
      zoom: 100,
      label: {
        emphasis: {
          show: false
        }
      },
      roam: true,
      itemStyle: {
        normal: {
          areaColor: "#323c48",
          borderColor: "#111"
        },
        emphasis: {
          areaColor: "#2a333d"
        }
      }
    },
     tooltip: {
     trigger: 'item',
        formatter: function (params) {
        return `${params.seriesName}<br />
                <b>${params.name}</b> <br />${params.data.value[2]} `;
        }
    },
    grid: {
      right: 40,
      top: 100,
      bottom: 40,
      width: "30%"
    },
    xAxis: {
      type: "value",
      scale: true,
      position: "top",
      boundaryGap: false,
      splitLine: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { margin: 2, textStyle: { color: "#aaa" } }
    },
    yAxis: {
      type: "category",
      name: "Specimen Type Distribution",
      nameGap: 16,
      axisLine: { show: false, lineStyle: { color: "#ddd" } },
      axisTick: { show: false, lineStyle: { color: "#ddd" } },
      axisLabel: { interval: 0, textStyle: { color: "#ddd" } },
      data: []
    },
    series: [
      {
        name: "Specimen",
        type: "effectScatter",
        coordinateSystem: "geo",
        data: convertedData[0],
        showEffectOn: "emphasis",
        rippleEffect: {
          brushType: "stroke"
        },
        hoverAnimation: true,
        label: {
          normal: {
            formatter: "{b}",
            position: "right",
            show: true
          }
        },
        itemStyle: {
          normal: {
            color: "#f4e925",
            shadowBlur: 10,
            shadowColor: "#333"
          }
        },
        zlevel: 1
      },
      {
        id: "bar",
        zlevel: 2,
        type: "bar",
        symbol: "none",
        itemStyle: {
          normal: {
            color: "#ddb926"
          }
        },
        data: []
      }
    ]
  };
  
  // Use just the specified configurations and data charts.
  chart.setOption(option);
  //const result = arr.reduce((acc, curr) => (acc[curr] = (acc[curr] || 0) + 1, acc), {});

  chart.on("brushselected", renderBrushed);
 
  
  function renderBrushed(params) {
    var mainSeries = params.batch[0].selected[0];
  
    var selectedItems = [];
    var categoryData = [];
    var barData = [];
    var maxBar = 30;
    var count = 0;
  
    for (var i = 0; i < mainSeries.dataIndex.length; i++) {
      var rawIndex = mainSeries.dataIndex[i];
      var dataItem = convertedData[0][rawIndex];
      var pmValue = dataItem.value[2];
  
      count++;
  
      selectedItems.push(dataItem);
    }
  
    selectedItems.sort(function (a, b) {
      return a.value[2] - b.value[2];
    });
  
    for (var i = 0; i < Math.min(selectedItems.length, maxBar); i++) {
      categoryData.push(selectedItems[i].value[2]);
      barData.push(selectedItems[i].value[2]);
    }
    result = barData.reduce((acc, curr) => (acc[curr] = (acc[curr] || 0) + 1, acc), {});


    this.setOption({
      yAxis: {
        data: Object.keys(result)
      },
      xAxis: {
        axisLabel: { show: !!count }
      },
      series: {
        id: "bar",
        data: Object.values(result)
      }
    });
  }
  