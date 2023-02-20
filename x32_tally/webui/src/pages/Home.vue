<template>
  <v-container fluid class="channel-group">
    <v-row  class="channel-group d-flex justify-center">
      <template v-for="channel in channels">
        <mixer-channel
            v-if="channel.enabled"
            :name="channel.name ? channel.name : `Ch ${channel.ch}`"
            :color="channel.color"
            :icon="channel.icon"
            :fader="channel.fader"
            :muted="channel.muted"
            :onStand="channel.onStand"
        ></mixer-channel>
      </template>
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
        1: {enabled: true, name: "Ch 01", color: 0, icon: 1, ch: 1, muted: false, fader: 0, onStand: null},
        2: {enabled: true, name: "Ch 02", color: 0, icon: 1, ch: 2, muted: false, fader: 0, onStand: null},
        3: {enabled: true, name: "Ch 03", color: 0, icon: 1, ch: 3, muted: false, fader: 0, onStand: null},
        4: {enabled: true, name: "Ch 04", color: 0, icon: 1, ch: 4, muted: false, fader: 0, onStand: null},
        5: {enabled: true, name: "Ch 05", color: 0, icon: 1, ch: 5, muted: false, fader: 0, onStand: null},
        6: {enabled: true, name: "Ch 06", color: 0, icon: 1, ch: 6, muted: false, fader: 0, onStand: null},
        7: {enabled: true, name: "Ch 07", color: 0, icon: 1, ch: 7, muted: false, fader: 0, onStand: null},
        8: {enabled: true, name: "Ch 08", color: 0, icon: 1, ch: 8, muted: false, fader: 0, onStand: null},
        9: {enabled: true, name: "Ch 09", color: 0, icon: 1, ch: 9, muted: false, fader: 0, onStand: null},
        10: {enabled: true, name: "Ch 10", color: 0, icon: 1, ch: 10, muted: false, fader: 0, onStand: null},
        11: {enabled: true, name: "Ch 11", color: 0, icon: 1, ch: 11, muted: false, fader: 0, onStand: null},
        12: {enabled: true, name: "Ch 12", color: 0, icon: 1, ch: 12, muted: false, fader: 0, onStand: null},
        13: {enabled: true, name: "Ch 13", color: 0, icon: 1, ch: 13, muted: false, fader: 0, onStand: null},
        14: {enabled: true, name: "Ch 14", color: 0, icon: 1, ch: 14, muted: false, fader: 0, onStand: null},
        15: {enabled: true, name: "Ch 15", color: 0, icon: 1, ch: 15, muted: false, fader: 0, onStand: null},
        16: {enabled: true, name: "Ch 16", color: 0, icon: 1, ch: 16, muted: false, fader: 0, onStand: null},
        17: {enabled: true, name: "Ch 17", color: 0, icon: 1, ch: 17, muted: false, fader: 0, onStand: null},
        18: {enabled: true, name: "Ch 18", color: 0, icon: 1, ch: 18, muted: false, fader: 0, onStand: null},
        19: {enabled: true, name: "Ch 19", color: 0, icon: 1, ch: 19, muted: false, fader: 0, onStand: null},
        20: {enabled: true, name: "Ch 20", color: 0, icon: 1, ch: 20, muted: false, fader: 0, onStand: null},
        21: {enabled: true, name: "Ch 21", color: 0, icon: 1, ch: 21, muted: false, fader: 0, onStand: null},
        22: {enabled: true, name: "Ch 22", color: 0, icon: 1, ch: 22, muted: false, fader: 0, onStand: null},
        23: {enabled: true, name: "Ch 23", color: 0, icon: 1, ch: 23, muted: false, fader: 0, onStand: null},
        24: {enabled: true, name: "Ch 24", color: 0, icon: 1, ch: 24, muted: false, fader: 0, onStand: null},
        25: {enabled: true, name: "Ch 25", color: 0, icon: 1, ch: 25, muted: false, fader: 0, onStand: null},
        26: {enabled: true, name: "Ch 26", color: 0, icon: 1, ch: 26, muted: false, fader: 0, onStand: null},
        27: {enabled: true, name: "Ch 27", color: 0, icon: 1, ch: 27, muted: false, fader: 0, onStand: null},
        28: {enabled: true, name: "Ch 28", color: 0, icon: 1, ch: 28, muted: false, fader: 0, onStand: null},
        29: {enabled: true, name: "Ch 29", color: 0, icon: 1, ch: 29, muted: false, fader: 0, onStand: null},
        30: {enabled: true, name: "Ch 30", color: 0, icon: 1, ch: 30, muted: false, fader: 0, onStand: null},
        31: {enabled: true, name: "Ch 31", color: 0, icon: 1, ch: 31, muted: false, fader: 0, onStand: null},
        32: {enabled: true, name: "Ch 32", color: 0, icon: 1, ch: 32, muted: false, fader: 0, onStand: null},
      }
    }
  },
  methods: {
    onMessage(data) {
      const topic = data.topic
      const message = JSON.parse(data.message)

      if(topic.startsWith("config/input_channels")) {
        for (const channel_n in message) {
          this.channels[channel_n].enabled = message[channel_n].enabled
        }
      }

      if(topic.startsWith("modules/osc/ch/")) {
        if(topic.endsWith("/mix/fader")) {
          let channel = parseInt(topic.replaceAll("modules/osc/ch/", "").replaceAll("/mix/fader", ""))
          this.channels[channel].fader = message[0]
        }
        if(topic.endsWith("/mix/on")) {
          let channel = parseInt(topic.replaceAll("modules/osc/ch/", "").replaceAll("/mix/on", ""))
          this.channels[channel].muted = !message[0]
        }
        if(topic.endsWith("/config/color")) {
          let channel = parseInt(topic.replaceAll("modules/osc/ch/", "").replaceAll("/config/color", ""))
          this.channels[channel].color = message[0]
        }
        if(topic.endsWith("/config/name")) {
          let channel = parseInt(topic.replaceAll("modules/osc/ch/", "").replaceAll("/config/name", ""))
          this.channels[channel].name = message[0]
        }
        if(topic.endsWith("/config/icon")) {
          let channel = parseInt(topic.replaceAll("modules/osc/ch/", "").replaceAll("/config/icon", ""))
          this.channels[channel].icon = message[0]
        }
      }
      if(topic.startsWith("modules/stand_buttons/")) {
        if (topic.endsWith("/status")) {
          let channel = parseInt(topic.replaceAll("modules/stand_buttons/", "").replaceAll("/status", ""))
          this.channels[channel].onStand = message.has_button && message.enabled ? message.value : null
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
    margin-top: 0;
  }
</style>