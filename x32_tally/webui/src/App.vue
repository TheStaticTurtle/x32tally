<template>

  <v-app theme="dark">
    <Navbar></Navbar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <CueDrawer style="margin-bottom: 16px"></CueDrawer>
    <v-footer class="footer" app>
      <a href="https://github.com/TheStaticTurtle/x32tally">X32Tally</a>&nbsp;&nbsp;-&nbsp;&nbsp;© 2023 TheStaticTurtle&nbsp;&nbsp;-&nbsp;&nbsp;Licensed under&nbsp;<a href="https://github.com/TheStaticTurtle/x32tally/blob/master/LICENSE.md">GPLv3.0</a>
    </v-footer>
  </v-app>
</template>

<script>
import * as mqtt from 'mqtt/dist/mqtt.min';
import EventBus from "@/eventBus"
import Navbar from "@/components/Navbar.vue";
import CueDrawer from "@/components/CueDrawer.vue";

export default {
  name: "App",
  components: {CueDrawer, Navbar},
  mounted() {
    let client = mqtt.connect(`ws://${document.location.host}/mqtt`, {
      clientId: "x32tally_web" + Math.random().toString(16).substr(2, 8)
    })

    client.on('error', function (err) {
      console.error(err)
      client.end()
    })

    client.on('connect', function () {
      console.info('Client connected')
      client.subscribe('#', { qos: 0 })
    })

    client.on('message', function (topic, message, packet) {
      EventBus.$emit("mqtt-message", {
        topic,
        message: message.toString()
      })
    })

    client.on('close', function () {
      console.warn('Disconnected')
    })
  }
}
</script>

<style scoped>
.footer {
  max-height: 16px !important;
  font-size: 0.70rem;
}
</style>
