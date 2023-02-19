<template>
  <v-container fluid class="channel-group">
    <v-row>
      <mixer-channel
          v-for="channel in channels"
          :name="channel.name ? channel.name : `Ch ${channel.ch}`"
          :color="channel.color"
          :icon="channel.icon"
          :fader="channel.fader"
          :muted="channel.muted"
          :onStand="channel.onStand"
      ></mixer-channel>
    </v-row>
  </v-container>
</template>

<script>
import MixerChannel from "@/components/MixerChannel.vue";
import EventBus from "@/eventBus"

export default {
  name: "Home",
  components: {MixerChannel},
  mounted() {
    EventBus.$on("mqtt-message", this.onMessage)
  },
  unmounted() {
    EventBus.$off("mqtt-message", this.onMessage)
  },
  data() {
    return {
      channels: {
        1: {name: "Ch 01", color: 0, icon: 1, ch: 1, muted: false, fader: 0, onStand: null},
        2: {name: "Ch 02", color: 0, icon: 1, ch: 2, muted: false, fader: 0, onStand: null},
        3: {name: "Ch 03", color: 0, icon: 1, ch: 3, muted: false, fader: 0, onStand: null},
        4: {name: "Ch 04", color: 0, icon: 1, ch: 4, muted: false, fader: 0, onStand: null},
        5: {name: "Ch 05", color: 0, icon: 1, ch: 5, muted: false, fader: 0, onStand: null},
        6: {name: "Ch 06", color: 0, icon: 1, ch: 6, muted: false, fader: 0, onStand: null},
        7: {name: "Ch 07", color: 0, icon: 1, ch: 7, muted: false, fader: 0, onStand: null},
        8: {name: "Ch 08", color: 0, icon: 1, ch: 8, muted: false, fader: 0, onStand: null},
        9: {name: "Ch 09", color: 0, icon: 1, ch: 9, muted: false, fader: 0, onStand: null},
        10: {name: "Ch 10", color: 0, icon: 1, ch: 10, muted: false, fader: 0, onStand: null},
        11: {name: "Ch 11", color: 0, icon: 1, ch: 11, muted: false, fader: 0, onStand: null},
        12: {name: "Ch 12", color: 0, icon: 1, ch: 12, muted: false, fader: 0, onStand: null},
        13: {name: "Ch 13", color: 0, icon: 1, ch: 13, muted: false, fader: 0, onStand: null},
        14: {name: "Ch 14", color: 0, icon: 1, ch: 14, muted: false, fader: 0, onStand: null},
        15: {name: "Ch 15", color: 0, icon: 1, ch: 15, muted: false, fader: 0, onStand: null},
        16: {name: "Ch 16", color: 0, icon: 1, ch: 16, muted: false, fader: 0, onStand: null},
        17: {name: "Ch 17", color: 0, icon: 1, ch: 17, muted: false, fader: 0, onStand: null},
        18: {name: "Ch 18", color: 0, icon: 1, ch: 18, muted: false, fader: 0, onStand: null},
        19: {name: "Ch 19", color: 0, icon: 1, ch: 19, muted: false, fader: 0, onStand: null},
        20: {name: "Ch 20", color: 0, icon: 1, ch: 20, muted: false, fader: 0, onStand: null},
        21: {name: "Ch 21", color: 0, icon: 1, ch: 21, muted: false, fader: 0, onStand: null},
        22: {name: "Ch 22", color: 0, icon: 1, ch: 22, muted: false, fader: 0, onStand: null},
        23: {name: "Ch 23", color: 0, icon: 1, ch: 23, muted: false, fader: 0, onStand: null},
        24: {name: "Ch 24", color: 0, icon: 1, ch: 24, muted: false, fader: 0, onStand: null},
        25: {name: "Ch 25", color: 0, icon: 1, ch: 25, muted: false, fader: 0, onStand: null},
        26: {name: "Ch 26", color: 0, icon: 1, ch: 26, muted: false, fader: 0, onStand: null},
        27: {name: "Ch 27", color: 0, icon: 1, ch: 27, muted: false, fader: 0, onStand: null},
        28: {name: "Ch 28", color: 0, icon: 1, ch: 28, muted: false, fader: 0, onStand: null},
        29: {name: "Ch 29", color: 0, icon: 1, ch: 29, muted: false, fader: 0, onStand: null},
        30: {name: "Ch 30", color: 0, icon: 1, ch: 30, muted: false, fader: 0, onStand: null},
        31: {name: "Ch 31", color: 0, icon: 1, ch: 31, muted: false, fader: 0, onStand: null},
        32: {name: "Ch 32", color: 0, icon: 1, ch: 32, muted: false, fader: 0, onStand: null},
      }
    }
  },
  methods: {
    onMessage(data) {
      const topic = data.topic
      const message = JSON.parse(data.message)

      if(topic.startsWith("X32/ch/")) {
        if(topic.endsWith("/mix/fader")) {
          let channel = parseInt(topic.replaceAll("X32/ch/", "").replaceAll("/mix/fader", ""))
          this.channels[channel].fader = 1 - message[0]
        }
        if(topic.endsWith("/mix/on")) {
          let channel = parseInt(topic.replaceAll("X32/ch/", "").replaceAll("/mix/on", ""))
          this.channels[channel].muted = !message[0]
        }
        if(topic.endsWith("/config/color")) {
          let channel = parseInt(topic.replaceAll("X32/ch/", "").replaceAll("/config/color", ""))
          this.channels[channel].color = message[0]
        }
        if(topic.endsWith("/config/name")) {
          let channel = parseInt(topic.replaceAll("X32/ch/", "").replaceAll("/config/name", ""))
          this.channels[channel].name = message[0]
        }
        if(topic.endsWith("/config/icon")) {
          let channel = parseInt(topic.replaceAll("X32/ch/", "").replaceAll("/config/icon", ""))
          this.channels[channel].icon = message[0]
        }
      }
      if(topic.startsWith("ONSTAND_DETECTION/ch/")) {
        if (topic.endsWith("/is_on_stand")) {
          let channel = parseInt(topic.replaceAll("ONSTAND_DETECTION/ch/", "").replaceAll("/is_on_stand", ""))
          this.channels[channel].onStand = message > 0
        }
      }
    }
  }
}

</script>

<style scoped>
  .channel-group {
    display: flex;
    flex-wrap: wrap;
  }
</style>