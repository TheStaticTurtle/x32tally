<template>
  <div class="mixer-channel" :class="{'channel-blink': blinking}">
    <div class="channel-name" :style="headerColor" :class="{'channel-blink': blinking}">
      {{ short_name }}
      <div :class="headerIcon" alt=""/>
    </div>
    <div class="channel-infos">
      <fader :value="fader"></fader>
    </div>
    <v-spacer></v-spacer>
    <led :enabled="!muted" >
      <v-icon v-if="muted" icon="mdi-microphone-off"></v-icon>
      <v-icon v-else icon="mdi-microphone"></v-icon>
    </led>
    <led v-if="onStand!=null" :enabled="!onStand" color-off="#fd7e14">
      <v-icon v-if="onStand" icon="mdi-wall"></v-icon>
      <v-icon v-else icon="mdi-face-agent"></v-icon>
    </led>
    <led v-else :enabled="false" color-off="gray"><v-icon icon="mdi-wall"></v-icon></led>
  </div>
</template>

<script>
import Led from "@/components/Led.vue";
import Fader from "@/components/Fader.vue";

import "../assets/x32icons.css"


export default {
  name: "MixerChannel",
  components: {Fader, Led},
  props: {
    name: {
      type: String,
      required: true
    },
    muted: {
      type: Boolean,
      required: true
    },
    fader: {
      type: Number,
      required: true
    },

    color: {
      type: Number,
      required: true
    },
    icon: {
      type: Number,
      default: 0
    },

    onStand: {
      type: Boolean,
      default: false
    },
  },

  computed: {
    short_name() {
      const len = 6;
      return this.name.length > len ? this.name.slice(0, len) + "…" : this.name;
    },

    blinking() {
      return (this.muted !== this.onStand) && this.onStand !== null
    },

    headerColor() {
      if(this.color === 0) return {"border-color": "gray"}
      if(this.color === 1) return {"border-color": "orangered"}
      if(this.color === 2) return {"border-color": "lawngreen"}
      if(this.color === 3) return {"border-color": "yellow"}
      if(this.color === 4) return {"border-color": "dodgerblue"}
      if(this.color === 5) return {"border-color": "magenta"}
      if(this.color === 6) return {"border-color": "cyan"}
      if(this.color === 7) return {"border-color": "lightgray"}
      if(this.color === 8) return {"border-color": "gray"}
      if(this.color === 9) return {"border-color": "orangered"}
      if(this.color === 10) return {"border-color": "lawngreen"}
      if(this.color === 11) return {"border-color": "yellow"}
      if(this.color === 12) return {"border-color": "dodgerblue"}
      if(this.color === 13) return {"border-color": "magenta"}
      if(this.color === 14) return {"border-color": "cyan"}
      if(this.color === 15) return {"border-color": "lightgray"}
    },
    headerIcon() {
      return "x32icon-"+this.icon
    }
  }
}
</script>

<style scoped>
  .mixer-channel {
    display: flex;
    height: 300px;
    width: 80px;
    border: 3px solid gray;
    border-radius: 8px;
    flex-direction: column;
    align-items: center;
    padding: 4px;
    margin: 4px;
  }
  .mixer-channel > .channel-name {
    display: flex;
    border: 3px solid gray;
    width: 80px;
    padding: 8px 8px 4px;
    margin-top: -8px;
    border-radius: 8px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .mixer-channel > .channel-name > div {
    height: 48px;
    width: 48px;
    background-size: cover;
    border: 1px solid gray;
    border-radius: 8px;
  }
  .mixer-channel > .channel-infos {
    width: 100%;
    height: 100%;
    padding: 6px 0;
    display: flex;
    flex-direction: row;
  }

  .channel-blink {
    animation: channel-blink-animation 0.50s steps(1, start) infinite;
    -webkit-animation: channel-blink-animation .50s steps(1, start) infinite;
  }
  @keyframes channel-blink-animation {
    50% {
      border: 3px yellow dashed;
    }
  }
  @-webkit-keyframes channel-blink-animation {
    50% {
      border: 3px yellow dashed;
    }
  }

</style>