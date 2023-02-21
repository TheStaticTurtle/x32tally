<template>
  <v-navigation-drawer permanent>
    <v-container class="pt-2 py-0 text-center">
      <h1>{{ show_name }}</h1>
    </v-container>
    <v-list density="compact">
      <v-list-item v-for="(cue, cue_key) in cues" :active="cue_key == current_cue">
        <h3 class="d-inline-block">{{ cue.id.combined }}</h3> - {{ cue.name }}
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import EventBus from "@/eventBus";
import logo from "@/assets/logo.png";
import {nextTick} from "vue";

export default {
  name: "CueDrawer",
  mounted() {
    EventBus.$on("mqtt-message", this.onMessage)
    this.update_interval = setInterval(this.update, 1000/30)
  },
  unmounted() {
    EventBus.$off("mqtt-message", this.onMessage)
  },
  data() {
    return {
      show_name: "Unknown show",
      current_cue: null,
      cues: {}
    }
  },
  methods: {
    processRawCueId(rid) {
      rid = rid.toString()
      let a = rid.substring(0, rid.length-2)
      let b = rid.charAt(rid.length-2)
      let c = rid.charAt(rid.length-1)
      return {
        a,b,c,
        combined: a + (b!="0" || c!="0" ? "." + b + (c!="0" ? "." + c : "") : "")
      }
    },
    onMessage(data) {
      const topic = data.topic
      const message = JSON.parse(data.message)

      if(topic.startsWith("modules/osc/-show/showfile/show")) {
        this.show_name = message[0]
      }
      if(topic.startsWith("modules/osc/-show/prepos/current")) {
        this.current_cue = parseInt(message[0])
      }
      if(topic.startsWith("modules/osc/-show/showfile/cue/")) {
        let cue_id = parseInt(topic.replaceAll("modules/osc/-show/showfile/cue/", ""))

        this.cues[cue_id] = {
          raw_id: message[0],
          id: this.processRawCueId(message[0]),
          name: message[1],
        }
      }//
    }
  }
}
</script>

<style scoped>

</style>