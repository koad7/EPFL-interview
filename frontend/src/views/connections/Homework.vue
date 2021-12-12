<template>
  <v-row>
    <v-col cols="6">
      <v-card>
        <v-card-title></v-card-title>
        <v-chart :option="mapOption" :loading="loading" ></v-chart>
      </v-card>
    </v-col>
    <v-col cols="6">
      <v-card>
        <v-card-title></v-card-title>
        <v-chart :option="specimenType" ></v-chart>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>
.echarts {
  min-height: 512px;
}
</style>

<script lang="ts">
import { Component,Vue, Watch } from "vue-property-decorator";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import {
  GridComponent,
  TitleComponent,
  TooltipComponent,
} from "echarts/components";
import { ScatterChart, EffectScatterChart } from "echarts/charts";
import { EChartsOption } from "echarts/types/dist/shared";
import * as echarts from "echarts";
import worldMap from "echarts-map/json/world.json";
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  ScatterChart,
  EffectScatterChart,
]);

interface DataItem {
  name: string;
  value: number[];
}
interface GeoCord {
  name: string;
  value: number[];
}

echarts.registerMap("world", worldMap);

const arrToInstanceCountObj = arr => arr.reduce((obj, e) => {
  obj[e] = (obj[e] || 0) + 1;
  return obj;
}, {});


@Component({
  components: {
    VChart,
  },
})
export default class Homework extends Vue {
  loading = true;
  geoCoordMap: DataItem[] = [];
  mapData: DataItem[] = [];
  convertedData: GeoCord[]=[]
  specimenTypeArr:string[] =[]
  specimenTypeList:string[] =[]

 @Watch("query")
  created(): void {
    this.loading = true;
      this.$connectionsApi
        .getConnections()
        .then((response) => response.data)
        .then((connections) => {
                 connections.items.filter(x => this.geoCoordMap.push({"name":x.id, "value":[ x.lon, x.lat, x.specimen_type]}));
                 connections.items.filter(item => {this.specimenTypeArr[item.id]=item.specimen_type})
                 this.specimenTypeList=Object.values(this.specimenTypeArr);
        })
        .finally(() => {
          this.loading = false;
        })
  }
  get specimenType(): EChartsOption {
    return {
      xAxis: {
        type: "category",
        data: Object.keys(arrToInstanceCountObj(this.specimenTypeList)),
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          data: Object.values(arrToInstanceCountObj(this.specimenTypeList)),
          type: "bar",
        },
      ]
    };
  }

  get mapOption(): EChartsOption {
    return {
    backgroundColor: "#404a59",
    animation: false,
    title: [
      {
        text: "Homework EPFL Full Stack",
        subtext: "Kodjo A.",
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
        borderColor: "#fff",
        emphasis: {
          
          iconStyle:{
              borderColor: "#fff",
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
      geoIndex: 0,
    },
    geo: {
      map: "world",
      left: "10",
      right: "35%",
      center: [6.633597, 46.519962],
      zoom: 100,
      emphasis: {
        label: {
          show: false
        }
      },
      roam: true,
      itemStyle: {
          areaColor: "#323c48",
          borderColor: "#111",
        emphasis: {
          areaColor: "#2a333d"
        }
      }
    },
     tooltip: {
     trigger: 'item',
        formatter: function (params:any) {
        return `
                <b>${params.name}</b> <br />${params.data.value[2]} `;
        }
    },
    grid: {
      right: 40,
      top: 100,
      bottom: 40,
      width: "50%"
    },
    xAxis: {
      type: "value",
      scale: true,
      position: "top",
      boundaryGap: false,
      splitLine: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { margin: 2 },
      // textStyle: { color: "#aaa" }
    },
    yAxis: {
      type: "category",
      name: "",
      nameGap: 16,
      axisLine: { show: false, lineStyle: { color: "#ddd" } },
      axisTick: { show: false, lineStyle: { color: "#ddd" } },
      axisLabel: { interval: 0},
      //  textStyle: { color: "#ddd" } 
      data: []
    },
    series: [
      {
        name: "Specimen",
        type: "effectScatter",
        coordinateSystem: "geo",
        data:  this.geoCoordMap,
        showEffectOn: "emphasis",
        rippleEffect: {
          brushType: "stroke"
        },
        label: {
            formatter: "{b}",
            position: "right",
            show: true
        },
        itemStyle: {
            color: "#f4e925",
            shadowBlur: 10,
            shadowColor: "#333"
        },
        zlevel: 1
   
      }
    ]
  }
  }
}
</script>
