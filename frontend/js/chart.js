document.addEventListener("DOMContentLoaded", function () {
  // 1️⃣ 첫 번째 차트
  (function () {
    var dom = document.getElementById("chart-container-1");
    var myChart = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });
    var app = {};

    var option;

    option = {
      color: ["#80FFA5", "#00DDFF", "#37A2FF", "#FF0087", "#FFBF00"],
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "cross",
          label: {
            backgroundColor: "#6a7985",
          },
        },
      },
      legend: {
        data: ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
      },
      toolbox: {
        feature: {
          saveAsImage: {},
        },
      },
      grid: {
        left: "3%",
        right: "4%",
        bottom: "3%",
        containLabel: true,
      },
      xAxis: [
        {
          type: "category",
          boundaryGap: false,
          data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
      ],
      yAxis: [
        {
          type: "value",
        },
      ],
      series: [
        {
          name: "Line 1",
          type: "line",
          stack: "Total",
          smooth: true,
          lineStyle: {
            width: 0,
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgb(128, 255, 165)",
              },
              {
                offset: 1,
                color: "rgb(1, 191, 236)",
              },
            ]),
          },
          emphasis: {
            focus: "series",
          },
          data: [140, 232, 101, 264, 90, 340, 250],
        },
        {
          name: "Line 2",
          type: "line",
          stack: "Total",
          smooth: true,
          lineStyle: {
            width: 0,
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgb(0, 221, 255)",
              },
              {
                offset: 1,
                color: "rgb(77, 119, 255)",
              },
            ]),
          },
          emphasis: {
            focus: "series",
          },
          data: [120, 282, 111, 234, 220, 340, 310],
        },
        {
          name: "Line 3",
          type: "line",
          stack: "Total",
          smooth: true,
          lineStyle: {
            width: 0,
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgb(55, 162, 255)",
              },
              {
                offset: 1,
                color: "rgb(116, 21, 219)",
              },
            ]),
          },
          emphasis: {
            focus: "series",
          },
          data: [320, 132, 201, 334, 190, 130, 220],
        },
        {
          name: "Line 4",
          type: "line",
          stack: "Total",
          smooth: true,
          lineStyle: {
            width: 0,
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgb(255, 0, 135)",
              },
              {
                offset: 1,
                color: "rgb(135, 0, 157)",
              },
            ]),
          },
          emphasis: {
            focus: "series",
          },
          data: [220, 402, 231, 134, 190, 230, 120],
        },
        {
          name: "Line 5",
          type: "line",
          stack: "Total",
          smooth: true,
          lineStyle: {
            width: 0,
          },
          showSymbol: false,
          label: {
            show: true,
            position: "top",
          },
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgb(255, 191, 0)",
              },
              {
                offset: 1,
                color: "rgb(224, 62, 76)",
              },
            ]),
          },
          emphasis: {
            focus: "series",
          },
          data: [220, 302, 181, 234, 210, 290, 150],
        },
      ],
    };

    if (option && typeof option === "object") {
      myChart.setOption(option);
    }

    window.addEventListener("resize", myChart.resize);
  })();

  (function () {
    var dom2 = document.getElementById("chart-container-2");
    var myChart2 = echarts.init(dom2, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });
    var app = {};

    var option;

    // See https://github.com/ecomfe/echarts-stat
    echarts.registerTransform(ecStat.transform.clustering);
    const data = [
      [3.275154, 2.957587],
      [-3.344465, 2.603513],
      [0.355083, -3.376585],
      [1.852435, 3.547351],
      [-2.078973, 2.552013],
      [-0.993756, -0.884433],
      [2.682252, 4.007573],
      [-3.087776, 2.878713],
      [-1.565978, -1.256985],
      [2.441611, 0.444826],
      [-0.659487, 3.111284],
      [-0.459601, -2.618005],
      [2.17768, 2.387793],
      [-2.920969, 2.917485],
      [-0.028814, -4.168078],
      [3.625746, 2.119041],
      [-3.912363, 1.325108],
      [-0.551694, -2.814223],
      [2.855808, 3.483301],
      [-3.594448, 2.856651],
      [0.421993, -2.372646],
      [1.650821, 3.407572],
      [-2.082902, 3.384412],
      [-0.718809, -2.492514],
      [4.513623, 3.841029],
      [-4.822011, 4.607049],
      [-0.656297, -1.449872],
      [1.919901, 4.439368],
      [-3.287749, 3.918836],
      [-1.576936, -2.977622],
      [3.598143, 1.97597],
      [-3.977329, 4.900932],
      [-1.79108, -2.184517],
      [3.914654, 3.559303],
      [-1.910108, 4.166946],
      [-1.226597, -3.317889],
      [1.148946, 3.345138],
      [-2.113864, 3.548172],
      [0.845762, -3.589788],
      [2.629062, 3.535831],
      [-1.640717, 2.990517],
      [-1.881012, -2.485405],
      [4.606999, 3.510312],
      [-4.366462, 4.023316],
      [0.765015, -3.00127],
      [3.121904, 2.173988],
      [-4.025139, 4.65231],
      [-0.559558, -3.840539],
      [4.376754, 4.863579],
      [-1.874308, 4.032237],
      [-0.089337, -3.026809],
      [3.997787, 2.518662],
      [-3.082978, 2.884822],
      [0.845235, -3.454465],
      [1.327224, 3.358778],
      [-2.889949, 3.596178],
      [-0.966018, -2.839827],
      [2.960769, 3.079555],
      [-3.275518, 1.577068],
      [0.639276, -3.41284],
    ];
    var CLUSTER_COUNT = 6;
    var DIENSIION_CLUSTER_INDEX = 2;
    var COLOR_ALL = [
      "#37A2DA",
      "#e06343",
      "#37a354",
      "#b55dba",
      "#b5bd48",
      "#8378EA",
      "#96BFFF",
    ];
    var pieces = [];
    for (var i = 0; i < CLUSTER_COUNT; i++) {
      pieces.push({
        value: i,
        label: "cluster " + i,
        color: COLOR_ALL[i],
      });
    }
    option = {
      toolbox: {
        show: true,
        // 버튼 위치 조정
        right: 20,
        top: 20,
        feature: {
          saveAsImage: {
            show: true,
            title: "차트 이미지 저장",
            type: "png",
            pixelRatio: 2,
          },
        },
      },
      dataset: [
        {
          source: data,
        },
        {
          transform: {
            type: "ecStat:clustering",
            // print: true,
            config: {
              clusterCount: CLUSTER_COUNT,
              outputType: "single",
              outputClusterIndexDimension: DIENSIION_CLUSTER_INDEX,
            },
          },
        },
      ],
      tooltip: {
        position: "top",
      },
      visualMap: {
        type: "piecewise",
        top: "middle",
        min: 0,
        max: CLUSTER_COUNT,
        left: 10,
        splitNumber: CLUSTER_COUNT,
        dimension: DIENSIION_CLUSTER_INDEX,
        pieces: pieces,
      },
      grid: {
        left: 120,
      },
      xAxis: {},
      yAxis: {},
      series: {
        type: "scatter",
        encode: { tooltip: [0, 1] },
        symbolSize: 15,
        itemStyle: {
          borderColor: "#555",
        },
        datasetIndex: 1,
      },
    };

    if (option && typeof option === "object") {
      myChart2.setOption(option);
    }

    window.addEventListener("resize", myChart2.resize);
  })();
});
