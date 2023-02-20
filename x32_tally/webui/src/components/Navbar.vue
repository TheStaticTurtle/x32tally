<template>
  <v-app-bar>
    <template v-slot:prepend>
      <v-app-bar-nav-icon>
        <v-img :src="logo" width="48px"></v-img>
      </v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>
      X32Tally
    </v-app-bar-title>
    <span class="text-center console-infos" :class="{'blinking': !osc_status.connected}">
      {{ osc_status.x32_server_name }} ({{ osc_status.x32_server_version }})<br>
      {{ osc_status.x32_console_model }} ({{ osc_status.x32_console_version }})<br>
      <template v-if="refresh">Last message: {{ osc_last_message_rel }}sec</template>
    </span>
    <v-spacer></v-spacer>

  </v-app-bar>
</template>

<script>
import logo from "../assets/logo.png"
import EventBus from "@/eventBus"
import {nextTick} from "vue";

export default {
  name: "Navbar",
  mounted() {
    EventBus.$on("mqtt-message", this.onMessage)
    this.update_interval = setInterval(this.update, 1000/30)
  },
  unmounted() {
    EventBus.$off("mqtt-message", this.onMessage)
    clearInterval(this.update_interval)
  },
  data() {
    return {
      logo,
      refresh: true,
      update_interval: null,

      osc_last_message: 0,
      osc_last_message_rel: 0,
      osc_status: {
        connected: true,
        x32_server_version: "V0.00",
        x32_server_name: "Unknown",
        x32_console_model: "Unknown",
        x32_console_version: "0.00"
      }
    }
  },
  methods: {
    update() {
      this.osc_last_message_rel = (Date.now() / 1000 - this.osc_last_message).toFixed(2)
    },
    onMessage(data) {
      const topic = data.topic
      const message = JSON.parse(data.message)

      if(topic.startsWith("modules/osc")) {
        this.osc_last_message = Date.now()/1000;
        if(topic.startsWith("modules/osc/status")) {
          this.osc_status = message
        }
      }
    },
    async forceRerender() {
      this.refresh = false;
      await nextTick();
      this.refresh = true;
    }
  }
}
</script>

<style scoped>
.console-infos {
  font-size: 0.8rem;
  color: #555;
  border-radius: 8px;
}
.blinking {
  font-weight: bold;
  animation: blink-animation 0.50s steps(1, start) infinite;
  -webkit-animation: blink-animation .50s steps(1, start) infinite;
}
@keyframes blink-animation {
  50% {
    color: red;
  }
}
@-webkit-keyframes blink-animation {
  50% {
    color: red;
  }
}
</style>