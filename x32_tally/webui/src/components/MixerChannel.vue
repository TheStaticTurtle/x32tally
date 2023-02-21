<template>
  <div class="mixer-channel" :style="channelColorStyle">
    <div class="channel-header" :style="headerColorStyle">
      <span class="channel-name">
        <fit-text>{{ name }}</fit-text>
      </span>
      <div class="header-icon" :class="headerIcon"/>
    </div>
    <div class="channel-infos">
      <fader :value="fader"></fader>
    </div>
    <v-spacer></v-spacer>
    <led :enabled="!muted" color-on="gray">
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
import FitText from "@/components/FitText.vue";


export default {
  name: "MixerChannel",
  components: {FitText, Fader, Led},
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
    active() {
      return !this.muted && this.fader > 0.08
    },

    active_on_stand() {
      return this.active && this.onStand
    },

    muted_in_hand() {
      return !this.active && !this.onStand
    },

    headerColorStyle() {
      if(this.active_on_stand) {
        return {
          "background-color": "#ffff00",
          "border-color": "#ffff00",
          "color": "#050504",
        }
      }
      if(this.muted_in_hand) {
        return {
          "background-color": "#00D0FFFF",
          "border-color": "#00D0FFFF",
          "color": "#050504",
        }
      }
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
    },
    channelColorStyle() {
      if(this.active_on_stand) {
        return {
          "border-color": "#ffff00",
        }
      }
      if(this.muted_in_hand) {
        return {
          "border-color": "#00D0FFFF",
        }
      }
      return {}
    }
  }
}
</script>

<style scoped>
  .mixer-channel {
    display: flex;
    height: 300px;
    width: 75px;
    border: 3px solid gray;
    border-radius: 8px;
    flex-direction: column;
    align-items: center;
    padding: 4px;
    margin: 6px;
  }
  .mixer-channel > .channel-header {
    display: flex;
    border: 3px solid gray;
    width: calc(100% + 14px);
    padding: 4px 8px 4px;
    margin-top: -7px;
    border-radius: 8px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .mixer-channel > .channel-header > div {
    height: 48px;
    width: 48px;
    background-size: cover;
    border-radius: 8px;
    border: 2px solid gray;
    background-color: rgb(var(--v-theme-background))
  }
  .mixer-channel > .channel-header > .channel-name {
    height: 20px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .mixer-channel > .channel-infos {
    width: 100%;
    height: 100%;
    padding: 6px 0;
    display: flex;
    flex-direction: row;
  }

</style>