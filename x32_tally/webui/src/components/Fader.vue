<template>
  <div class="fader">
    <div class="track">
      <div :style="top_style" class="fader-button"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Fader",
  props: {
    value: {
      type: Number,
      required: true
    },
  },
  computed: {
    top_style() {
      return {
        "top": (1 - this.value) * 100 + "%"
      }
    }
  }
}
</script>

<style scoped>
  .fader {
    display: flex;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
  }
  .track {
    background-color: #2d2d2d;
    width: 4px;
    height: calc(100% - 16px);
    display: flex;
    position: relative;
  }
  .fader-button {
    position: absolute;
    background-color: #464749;
    border: 2px solid gray;
    border-radius: 4px;
    width: 32px;
    height: 16px;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
  }
</style>