<template>

  <v-app theme="dark">
    <v-app-bar>
      <v-app-bar-title>X32Tally</v-app-bar-title>
      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import * as mqtt from 'mqtt/dist/mqtt.min';
import EventBus from "@/eventBus"

export default {
  name: "App",
  mounted() {
    let client = mqtt.connect(`ws://${document.location.host}/mqtt`) // create a client
    client.on('error', function (err) {
      console.log(err)
      client.end()
    })

    client.on('connect', function () {
      console.log('Client connected')
      client.subscribe('#', { qos: 0 })
    })

    client.on('message', function (topic, message, packet) {
      EventBus.$emit("mqtt-message", {
        topic,
        message: message.toString()
      })
    })

    client.on('close', function () {
      console.log('Disconnected')
    })
  }
}
</script>

<style scoped>

</style>
