<template>
  <div class="some-tips">
    <div class="tool"></div>
    <div class="tips">
      找到约{{SearchResult.totalNums}}个结果(用时{{SearchResult.searchCostTime}}秒)
    </div>
  </div>
</template>

<script>
import store from "@/store/index.js";
import { mapState, mapMutations } from "vuex";
export default {
computed: {
  ...mapState(['SearchResult'])
}
}
</script>

<style lang="less" scoped>
.some-tips{
  // .tool{
  //   border-bottom: 1px solid #999;
  // }
  .tips{
    text-align: left;
    padding-left: 1.5rem;
  }
}
</style>