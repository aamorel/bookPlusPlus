<template lang="html">
  <div class="header">
    <h1 class="book">book ++</h1>
    <p class="pa">Read with style</p>
    <div class="grid">


      <img class="img" src="../assets/logo.svg">

    </div>
  </div>
</template>

<script>



export default {
  name: 'Head',

}

</script>

<style lang="css" scoped>
.header {
  height: 100px;
  padding: 10px;
  text-align: center;
  background: #1abc9c;
  color: white;
  font-size: 20px;
  margin-bottom: 30px;
  margin-top: 0px;
  position: relative;
  border-radius: 10px
}
.img{
  position: absolute;
  top: -186px;
  left: -162px;
  width: 48%;
  display: block;
}
.book{
  margin-right: 518px;
  margin-top: -7px;
  align-self: flex-start;
  font-size: 70px;
  font-family: 'Manjari', sans-serif;
}
.pa{
  align-self: flex-start;
  margin-top: -25px;
  margin-right: 515px;
  font-family: 'Mansalva', cursive;
}
.grid {
  display: flex;
  max-width: 800px;
  margin: auto;
  overflow: hidden;
}

.cols {
  width: 50%;
  margin: 30px;

}
</style>
