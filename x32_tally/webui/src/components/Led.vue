<template>
  <span :style="style" class="led channel-mute">
    <slot></slot>
  </span>
</template>

<script>
export default {
  name: "Led",
  props: {
    enabled: {
      type: Boolean,
      required: true
    },
    colorOn: {
      type: String,
      default: "#198754"
    },
    colorOff: {
      type: String,
      default: "#dc3545"
    }
  },
  computed: {
    style() {
      return {
        "background-color": this.enabled ? this.colorOn : this.colorOff
      }
    }
  }
}
</script>

<style scoped>
  .led {
    display: flex;
    height: 40px;
    width: 100%;
    margin: 2px;
    padding: 4px;
    background-color: dimgray;
    border-radius: 4px;
    align-items: center;
    justify-content: center;
  }
</style>